#!/usr/bin/env python3
"""
Session Catchup Script for planning-with-files

Session-agnostic scanning: finds the most recent planning file update across
ALL sessions, then collects all conversation from that point forward through
all subsequent sessions until now.

Usage: python3 session-catchup.py [project-path]
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

PLANNING_FILES = ['task_plan.md', 'progress.md', 'findings.md']


def get_project_dir(project_path: str) -> Optional[Path]:
    """
    获取项目会话存储目录，支持多种IDE环境。
    按优先级尝试：环境变量 -> Trae -> Claude -> Cursor -> 其他
    """
    # 标准化项目路径
    sanitized = project_path.replace('/', '-').replace('\\', '-')
    if not sanitized.startswith('-'):
        sanitized = '-' + sanitized
    sanitized = sanitized.replace('_', '-')
    
    # 尝试多个可能的存储位置（按优先级排序）
    possible_roots = []
    
    # 1. 优先尝试环境变量指定的路径（用户自定义优先级最高）
    if 'TRAIDE_PLUGIN_ROOT' in os.environ:
        possible_roots.append(Path(os.environ['TRAIDE_PLUGIN_ROOT']) / 'projects')
    if 'CLAUDE_PLUGIN_ROOT' in os.environ:
        possible_roots.append(Path(os.environ['CLAUDE_PLUGIN_ROOT']) / 'projects')
    if 'CURSOR_PLUGIN_ROOT' in os.environ:
        possible_roots.append(Path(os.environ['CURSOR_PLUGIN_ROOT']) / 'projects')
    
    # 2. 尝试 Trae IDE 路径
    if 'USERPROFILE' in os.environ:
        possible_roots.append(Path(os.environ['USERPROFILE']) / '.trae' / 'projects')
    if 'HOME' in os.environ:
        possible_roots.append(Path(os.environ['HOME']) / '.trae' / 'projects')
    
    # 3. 尝试 Claude 路径
    if 'USERPROFILE' in os.environ:
        possible_roots.append(Path(os.environ['USERPROFILE']) / '.claude' / 'projects')
    if 'HOME' in os.environ:
        possible_roots.append(Path(os.environ['HOME']) / '.claude' / 'projects')
        
    # 4. 尝试 Cursor 路径
    if 'USERPROFILE' in os.environ:
        possible_roots.append(Path(os.environ['USERPROFILE']) / '.cursor' / 'projects')
    if 'HOME' in os.environ:
        possible_roots.append(Path(os.environ['HOME']) / '.cursor' / 'projects')
    
    # 5. 尝试 VS Code 路径
    if 'USERPROFILE' in os.environ:
        possible_roots.append(Path(os.environ['USERPROFILE']) / '.vscode' / 'projects')
    if 'HOME' in os.environ:
        possible_roots.append(Path(os.environ['HOME']) / '.vscode' / 'projects')
    
    # 查找第一个存在的项目目录
    for root in possible_roots:
        if not root.exists():
            continue
        project_dir = root / sanitized
        if project_dir.exists():
            return project_dir
    
    # 如果都没找到，返回第一个可能的路径（用于后续错误提示）
    if possible_roots:
        return possible_roots[0] / sanitized
    
    return None


def get_sessions_sorted(project_dir: Path) -> List[Path]:
    """Get all session files sorted by modification time (newest first)."""
    if not project_dir.exists():
        return []
    sessions = list(project_dir.glob('*.jsonl'))
    main_sessions = [s for s in sessions if not s.name.startswith('agent-')]
    return sorted(main_sessions, key=lambda p: p.stat().st_mtime, reverse=True)


def get_session_first_timestamp(session_file: Path) -> Optional[str]:
    """Get the timestamp of the first message in a session."""
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    ts = data.get('timestamp')
                    if ts:
                        return ts
                except:
                    continue
    except:
        pass
    return None


def scan_for_planning_update(session_file: Path) -> Tuple[int, Optional[str]]:
    """
    Quickly scan a session file for planning file updates.
    Returns (line_number, filename) of last update, or (-1, None) if none found.
    """
    last_update_line = -1
    last_update_file = None

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                if '"Write"' not in line and '"SearchReplace"' not in line:
                    continue

                try:
                    data = json.loads(line)
                    if data.get('type') != 'assistant':
                        continue

                    content = data.get('message', {}).get('content', [])
                    if not isinstance(content, list):
                        continue

                    for item in content:
                        if item.get('type') != 'tool_use':
                            continue
                        tool_name = item.get('name', '')
                        if tool_name not in ('Write', 'SearchReplace'):
                            continue

                        file_path = item.get('input', {}).get('file_path', '')
                        for pf in PLANNING_FILES:
                            if file_path.endswith(pf):
                                last_update_line = line_num
                                last_update_file = pf
                                break
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return last_update_line, last_update_file


def extract_messages_from_session(session_file: Path, after_line: int = -1) -> List[Dict]:
    """
    Extract conversation messages from a session file.
    If after_line >= 0, only extract messages after that line.
    If after_line < 0, extract all messages.
    """
    result = []

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                if after_line >= 0 and line_num <= after_line:
                    continue

                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = msg.get('type')
                is_meta = msg.get('isMeta', False)

                if msg_type == 'user' and not is_meta:
                    content = msg.get('message', {}).get('content', '')
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                content = item.get('text', '')
                                break
                        else:
                            content = ''

                    if content and isinstance(content, str):
                        # Skip system/command messages
                        if content.startswith(('<local-command', '<command-', '<task-notification')):
                            continue
                        if len(content) > 20:
                            result.append({
                                'role': 'user',
                                'content': content,
                                'line': line_num,
                                'session': session_file.stem[:8]
                            })

                elif msg_type == 'assistant':
                    msg_content = msg.get('message', {}).get('content', '')
                    text_content = ''
                    tool_uses = []

                    if isinstance(msg_content, str):
                        text_content = msg_content
                    elif isinstance(msg_content, list):
                        for item in msg_content:
                            if item.get('type') == 'text':
                                text_content = item.get('text', '')
                            elif item.get('type') == 'tool_use':
                                tool_name = item.get('name', '')
                                tool_input = item.get('input', {})
                                if tool_name == 'SearchReplace':
                                    tool_uses.append(f"Edit: {tool_input.get('file_path', 'unknown')}")
                                elif tool_name == 'Write':
                                    tool_uses.append(f"Write: {tool_input.get('file_path', 'unknown')}")
                                elif tool_name == 'RunCommand':
                                    cmd = tool_input.get('command', '')[:80]
                                    tool_uses.append(f"Command: {cmd}")
                                elif tool_name == 'AskUserQuestion':
                                    tool_uses.append("AskUserQuestion")
                                else:
                                    tool_uses.append(f"{tool_name}")

                    if text_content or tool_uses:
                        result.append({
                            'role': 'assistant',
                            'content': text_content[:600] if text_content else '',
                            'tools': tool_uses,
                            'line': line_num,
                            'session': session_file.stem[:8]
                        })
    except Exception:
        pass

    return result


def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    project_dir = get_project_dir(project_path)

    if not project_dir:
        print("[planning-with-files] INFO: Could not determine project storage location")
        print("  This is normal for new projects or if IDE session storage is not available.")
        print("  Tips:")
        print("    - Set TRAIDE_PLUGIN_ROOT or CLAUDE_PLUGIN_ROOT environment variable")
        print("    - Or ensure the IDE has created session storage")
        return

    if not project_dir.exists():
        print(f"[planning-with-files] INFO: No previous sessions found for: {project_path}")
        print(f"  (Checked: {project_dir})")
        print("  This is normal for new projects.")
        return

    sessions = get_sessions_sorted(project_dir)
    if len(sessions) < 2:
        return

    # Skip the current session (most recently modified = index 0)
    previous_sessions = sessions[1:]

    # Find the most recent planning file update across ALL previous sessions
    # Sessions are sorted newest first, so we scan in order
    update_session = None
    update_line = -1
    update_file = None
    update_session_idx = -1

    for idx, session in enumerate(previous_sessions):
        line, filename = scan_for_planning_update(session)
        if line >= 0:
            update_session = session
            update_line = line
            update_file = filename
            update_session_idx = idx
            break

    if not update_session:
        # No planning file updates found in any previous session
        return

    # Collect ALL messages from the update point forward, across all sessions
    all_messages = []

    # 1. Get messages from the session with the update (after the update line)
    messages_from_update_session = extract_messages_from_session(update_session, after_line=update_line)
    all_messages.extend(messages_from_update_session)

    # 2. Get ALL messages from sessions between update_session and current
    # These are sessions[1:update_session_idx] (newer than update_session)
    intermediate_sessions = previous_sessions[:update_session_idx]

    # Process from oldest to newest for correct chronological order
    for session in reversed(intermediate_sessions):
        messages = extract_messages_from_session(session, after_line=-1)  # Get all messages
        all_messages.extend(messages)

    if not all_messages:
        return

    # Output catchup report
    print("\n[planning-with-files] SESSION CATCHUP DETECTED")
    print(f"Last planning update: {update_file} in session {update_session.stem[:8]}...")

    sessions_covered = update_session_idx + 1
    if sessions_covered > 1:
        print(f"Scanning {sessions_covered} sessions for unsynced context")

    print(f"Unsynced messages: {len(all_messages)}")

    print("\n--- UNSYNCED CONTEXT ---")

    # Show up to 100 messages
    MAX_MESSAGES = 100
    if len(all_messages) > MAX_MESSAGES:
        print(f"(Showing last {MAX_MESSAGES} of {len(all_messages)} messages)\n")
        messages_to_show = all_messages[-MAX_MESSAGES:]
    else:
        messages_to_show = all_messages

    current_session = None
    for msg in messages_to_show:
        # Show session marker when it changes
        if msg.get('session') != current_session:
            current_session = msg.get('session')
            print(f"\n[Session: {current_session}...]")

        if msg['role'] == 'user':
            print(f"USER: {msg['content'][:300]}")
        else:
            if msg.get('content'):
                print(f"CLAUDE: {msg['content'][:300]}")
            if msg.get('tools'):
                print(f"  Tools: {', '.join(msg['tools'][:4])}")

    print("\n--- RECOMMENDED ---")
    print("1. Run: git diff --stat")
    print("2. Read: task_plan.md, progress.md, findings.md")
    print("3. Update planning files based on above context")
    print("4. Continue with task")


if __name__ == '__main__':
    main()
