param([string]$pptx, [string]$outDir)
# PowerPoint로 PPT를 열어 슬라이드마다 PNG로 저장 (화면 확인용)
New-Item -ItemType Directory -Force $outDir | Out-Null
Get-ChildItem $outDir -Filter *.png | Remove-Item -Force
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$i = 1
foreach ($s in $pres.Slides) {
    $s.Export((Join-Path $outDir ("slide{0:D2}.png" -f $i)), "PNG", 1600, 900)
    $i++
}
$pres.Close()
$app.Quit()
"exported $($i - 1)"
