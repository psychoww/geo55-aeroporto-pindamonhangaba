# Linhas de amostragem (seções transversais) da PPD em todas as estacas do memorial + seções das superfícies.
$ErrorActionPreference = 'Stop'
$AQUI = $PSScriptRoot
$E = Get-Content -Raw -Encoding UTF8 (Join-Path $AQUI 'civil3d\estacas.json') | ConvertFrom-Json
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$civ = $acad.GetInterfaceObject('AeccXUiLand.AeccApplication.13.9'); $cdoc = $civ.ActiveDocument; $adoc = $acad.ActiveDocument
try { $l = $adoc.Layers.Item('SECOES-PPD') } catch { $l = $adoc.Layers.Add('SECOES-PPD') }; $l.color = 4
$al = $cdoc.AlignmentsSiteless.Item('EIXO PPD 06-24')
for ($i = $al.SampleLineGroups.Count - 1; $i -ge 0; $i--) { $al.SampleLineGroups.Remove($i) }
# restos de vistas/secoes de rodadas anteriores
$apagar = @(); foreach ($ent in $adoc.ModelSpace) { if ($ent.ObjectName -in 'AeccDbGraphCrossSection', 'AeccDbSection', 'AeccDbSampleLine') { $apagar += $ent } }
foreach ($ent in $apagar) { try { $ent.Delete() } catch {} }; "objetos antigos apagados: " + $apagar.Count
$gps = $cdoc.GroupPlotStyles.Item(0); $sls = $cdoc.SampleLineStyles.Item(0); $lbl = $cdoc.SampleLineLabelStyles.Item(0)
$slg = $al.SampleLineGroups.Add('SL - PPD', 'SECOES-PPD', $gps, $sls, $lbl)
$w = [double]$E.largura
foreach ($est in $E.estacas) {
    $nome = if ($est[1]) { "{0} ({1})" -f $est[2], $est[1] } else { [string]$est[2] }
    [void]$slg.SampleLines.AddByStation($nome, [double]$est[0], $w, $w)
}
"linhas de amostragem: " + $slg.SampleLines.Count + "  (largura " + $w + " m para cada lado)"
$stEG = $cdoc.SectionStyles.Item('Existing Ground'); $stFG = $cdoc.SectionStyles.Item('Finished Ground')
foreach ($n in 'TN', 'TN_limpo', 'TERRAPLENAGEM', 'ACABADA') {
    $s = $cdoc.Surfaces.Item($n)
    $st = if ($n -like 'TN*') { $stEG } else { $stFG }
    [void]$slg.SampledSurfaces.Add($s, $st)
}
# o flag Sample vem desligado: sem ele as secoes nao sao criadas
for ($i = 0; $i -lt $slg.SampledSurfaces.Count; $i++) { $ss = $slg.SampledSurfaces.Item($i); $ss.Sample = $true; $ss.UpdateMode = 1 }
$slg.CreateSectionsAtSampleLines()
# secoes dinamicas (StaticDynamic = 0): so assim o COM devolve a geometria (ElevationAt, LengthLeft/Right)
for ($i = 0; $i -lt $slg.SampleLines.Count; $i++) { $l2 = $slg.SampleLines.Item($i); for ($j = 0; $j -lt $l2.Sections.Count; $j++) { $x = $l2.Sections.Item($j); $x.StaticDynamic = 0; $x.Update() } }
$sl = $slg.SampleLines.Item(0)
"secoes na 1a linha: " + $sl.Sections.Count
$adoc.Save(); 'salvo'
