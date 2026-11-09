# Vistas de seção (section views) de todas as linhas de amostragem, em grade abaixo do perfil longitudinal.
param([int]$Colunas = 6, [double]$Dx = 480.0, [double]$Dy = 340.0, [switch]$SoFaltantes)
$ErrorActionPreference = 'Stop'
$P = Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot 'civil3d\projeto.json') | ConvertFrom-Json
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$civ = $acad.GetInterfaceObject('AeccXUiLand.AeccApplication.13.9'); $cdoc = $civ.ActiveDocument; $adoc = $acad.ActiveDocument
try { $l = $adoc.Layers.Item('VISTAS-SECOES') } catch { $l = $adoc.Layers.Add('VISTAS-SECOES') }
$al = $cdoc.AlignmentsSiteless.Item('EIXO PPD 06-24'); $slg = $al.SampleLineGroups.Item('SL - PPD')
$sty = $cdoc.SectionViewStyles.Item('Road Section'); $sty.GraphStyle.VerticalExaggeration = 5.0
$bds = $null; foreach ($b in $cdoc.SectionViewBandStyleSets) { if ($b.Name -eq 'Offsets Only') { $bds = $b } }; if (-not $bds) { $bds = $cdoc.SectionViewBandStyleSets.Item(0) }
if (-not $SoFaltantes) {
    # SectionViews.Remove nao apaga a entidade: apaga todas as vistas de secao pelo espaco do modelo
    $apagar = @(); foreach ($e in $adoc.ModelSpace) { if ($e.ObjectName -eq 'AeccDbGraphCrossSection') { $apagar += $e } }
    foreach ($e in $apagar) { $e.Delete() }; "vistas antigas apagadas: " + $apagar.Count
}
$falhas = @(); $x0 = [double]$P.img.x0; $y0 = [double]$P.img.y0 - 1400.0
for ($i = 0; $i -lt $slg.SampleLines.Count; $i++) {
    $sl = $slg.SampleLines.Item($i)
    if ($SoFaltantes -and $sl.SectionViews.Count -gt 0) { continue }
    $c = $i % $Colunas; $r = [Math]::Floor($i / $Colunas)
    $xx = $x0 + $c * $Dx; $yy = $y0 - $r * $Dy
    $loc = [double[]]@($xx, $yy, 0.0)
    $ok = $false
    for ($t = 0; $t -lt 5 -and -not $ok; $t++) {
        try { [void]$sl.SectionViews.Add('Secao ' + $sl.Name, 'VISTAS-SECOES', $loc, $sty, $bds); $ok = $true }
        catch { Start-Sleep -Milliseconds (400 * ($t + 1)) }
    }
    if (-not $ok) { $falhas += $sl.Name }
}
if ($falhas.Count) { "falhas: " + ($falhas -join ', ') }
$v = $slg.SampleLines.Item(50).SectionViews.Item(0); $mn = $null; $mx = $null; $v.GetBoundingBox([ref]$mn, [ref]$mx)
"vistas criadas: {0}; caixa de uma vista: {1:F0} x {2:F0} m" -f $slg.SampleLines.Count, ($mx[0] - $mn[0]), ($mx[1] - $mn[1])
"bandas: " + $bds.Name + " | estilo: " + $sty.Name
$adoc.Save(); 'salvo'
