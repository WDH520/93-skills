---
name: remotion
description: |
  【触发关键词】Remotion、视频动画、React视频、MP4生成、
  代码生成视频、视频创作、动画制作、Remotion video、
  React video、video animation、MP4 creation、
  code video、video generation
  
  【适用场景】当用户需要使用Remotion框架、通过React代码生成MP4视频、
  进行视频创作、动画合成和渲染时使用。
  
  【核心功能】React驱动视频创作、MP4生成、动画合成、
  视频渲染、数据驱动视频、程序化内容生成。
---

# Remotion 视频动画创作

React驱动的视频创作框架，用代码生成MP4视频。

## 何时使用

- 创建数据驱动的视频（图表动画、报告视频）
- 需要程序化生成的内容（批量生成、参数化视频）
- 与React生态集成（使用现有组件、API数据）
- 需要版本控制的视频项目

## 快速开始

```bash
# 安装
npm install remotion @remotion/cli

# 启动开发服务器
npx remotion studio

# 渲染视频
npx remotion render src/index.ts MyVideo output.mp4
```

基础组件示例：

```tsx
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export const MyVideo = () => {
  const frame = useCurrentFrame(); // 当前帧号
  
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      <h1 style={{ color: 'white', opacity: frame / 30 }}>
        淡入文本
      </h1>
    </AbsoluteFill>
  );
};
```

详见 [rules/quickstart.md](rules/quickstart.md) 完整入门指南。

## 核心概念

| 概念 | 说明 | 参考 |
|------|------|------|
| Composition | 视频合成定义（时长、尺寸、组件） | [compositions.md](rules/compositions.md) |
| useCurrentFrame | 获取当前帧号驱动动画 | [animations.md](rules/animations.md) |
| Sequence | 时间轴分段管理 | [sequencing.md](rules/sequencing.md) |
| interpolate | 数值插值函数 | [timing.md](rules/timing.md) |

## 常见任务速查

### 媒体处理
- **图片**: [images.md](rules/images.md) - Img组件、静态文件引用
- **视频**: [videos.md](rules/videos.md) - 嵌入、裁剪、调速
- **音频**: [audio.md](rules/audio.md) - 音量控制、淡入淡出
- **GIF**: [gifs.md](rules/gifs.md) - 同步播放

### 动画效果
- **基础动画**: [animations.md](rules/animations.md) - useCurrentFrame、弹簧动画
- **文本动画**: [text-animations.md](rules/text-animations.md) - 打字机、文字逐行显示
- **转场**: [transitions.md](rules/transitions.md) - 场景切换效果
- **时间控制**: [timing.md](rules/timing.md) - 缓动函数、插值

### 高级功能
- **3D内容**: [3d.md](rules/3d.md) - Three.js集成
- **Lottie**: [lottie.md](rules/lottie.md) - After Effects动画
- **图表**: [charts.md](rules/charts.md) - 数据可视化
- **字幕**: [subtitles.md](rules/subtitles.md) - SRT字幕处理

### 工具函数
- **视频信息**: [get-video-duration.md](rules/get-video-duration.md)、[get-video-dimensions.md](rules/get-video-dimensions.md)
- **字体加载**: [fonts.md](rules/fonts.md) - Google Fonts、本地字体
- **DOM测量**: [measuring-dom-nodes.md](rules/measuring-dom-nodes.md)、[measuring-text.md](rules/measuring-text.md)

## 最佳实践

详见 [rules/best-practices.md](rules/best-practices.md)

1. **始终用 `useCurrentFrame()` 驱动动画**，禁用CSS动画
2. **时间以秒思考**，乘以fps转换为帧：`const frame = timeInSeconds * fps`
3. **使用 `staticFile()`** 引用本地资源，确保路径正确
4. **用 `Sequence` 分割** 复杂场景，便于管理时间轴
5. **添加类型定义**，使用Zod schema进行参数验证

## 扩展包安装

```bash
# 转场效果
npx remotion add @remotion/transitions

# 3D支持
npx remotion add @remotion/three

# Lottie动画
npx remotion add @remotion/lottie

# 光效叠加
npx remotion add @remotion/light-leaks
```

## 完整规则索引

- [3d.md](rules/3d.md) - 3D内容 (Three.js)
- [animations.md](rules/animations.md) - 基础动画
- [assets.md](rules/assets.md) - 资源导入
- [audio.md](rules/audio.md) - 音频处理
- [calculate-metadata.md](rules/calculate-metadata.md) - 动态元数据
- [can-decode.md](rules/can-decode.md) - 视频解码检测
- [charts.md](rules/charts.md) - 图表可视化
- [compositions.md](rules/compositions.md) - 合成定义
- [extract-frames.md](rules/extract-frames.md) - 帧提取
- [fonts.md](rules/fonts.md) - 字体加载
- [gifs.md](rules/gifs.md) - GIF动画
- [images.md](rules/images.md) - 图片嵌入
- [light-leaks.md](rules/light-leaks.md) - 光效
- [lottie.md](rules/lottie.md) - Lottie动画
- [maps.md](rules/maps.md) - 地图集成
- [measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - DOM测量
- [measuring-text.md](rules/measuring-text.md) - 文本测量
- [parameters.md](rules/parameters.md) - 参数化视频
- [sequencing.md](rules/sequencing.md) - 时间轴控制
- [subtitles.md](rules/subtitles.md) - 字幕处理
- [tailwind.md](rules/tailwind.md) - TailwindCSS
- [text-animations.md](rules/text-animations.md) - 文本动画
- [timing.md](rules/timing.md) - 时间插值
- [transitions.md](rules/transitions.md) - 转场效果
- [transparent-videos.md](rules/transparent-videos.md) - 透明视频
- [trimming.md](rules/trimming.md) - 裁剪
- [videos.md](rules/videos.md) - 视频嵌入
