# Check if all phases in task_plan.md are complete
# Exit 0 if complete, exit 1 if incomplete
# Used by Stop hook to verify task completion

param(
    [string]$PlanFile = "task_plan.md"
)

if (-not (Test-Path $PlanFile)) {
    Write-Host "ERROR: $PlanFile not found" -ForegroundColor Red
    Write-Host "Cannot verify completion without a task plan."
    exit 1
}

Write-Host "=== Task Completion Check ===" -ForegroundColor Cyan
Write-Host ""

$content = Get-Content $PlanFile -Raw

# Count phases by status
$total = ([regex]::Matches($content, "### Phase")).Count
$complete = ([regex]::Matches($content, "\*\*Status:\*\* complete")).Count
$inProgress = ([regex]::Matches($content, "\*\*Status:\*\* in_progress")).Count
$pending = ([regex]::Matches($content, "\*\*Status:\*\* pending")).Count

Write-Host "Total phases:   $total"
Write-Host "Complete:       $complete" -ForegroundColor Green
Write-Host "In progress:    $inProgress" -ForegroundColor Yellow
Write-Host "Pending:        $pending" -ForegroundColor Gray
Write-Host ""

# Check completion
if ($complete -eq $total -and $total -gt 0) {
    Write-Host "ALL PHASES COMPLETE" -ForegroundColor Green
    exit 0
} else {
    Write-Host "TASK NOT COMPLETE" -ForegroundColor Red
    Write-Host ""
    Write-Host "Do not stop until all phases are complete." -ForegroundColor Yellow
    exit 1
}
