# Monta o modelo da PPD no Aeroporto_PPD_Civil3D.dwg aberto no Civil 3D 2027 (via COM).
# Uso: powershell -ExecutionPolicy Bypass -File civil3d_aeroporto.ps1 [-Etapa superficies|imagem|alinhamento|todas]
param([string]$Etapa = 'todas')
$ErrorActionPreference = 'Stop'
$AQUI = $PSScriptRoot
$P = Get-Content -Raw -Encoding UTF8 (Join-Path $AQUI 'civil3d\projeto.json') | ConvertFrom-Json

$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$adoc = $null; foreach ($d in $acad.Documents) { if ($d.Name -like 'Aeroporto_PPD_Civil3D*.dwg') { $adoc = $d } }
if (-not $adoc) { throw 'Aeroporto_PPD_Civil3D.dwg nao esta aberto' }
if ($acad.ActiveDocument.Name -ne $adoc.Name) { $adoc.Activate(); Start-Sleep 1 }
$civ = $acad.GetInterfaceObject('AeccXUiLand.AeccApplication.13.9')
$cdoc = $civ.ActiveDocument

function Camada($nome, $cor) { try { $l = $adoc.Layers.Item($nome) } catch { $l = $adoc.Layers.Add($nome) }; $l.color = $cor; return $l }
function PorNome($colecao, $padrao) { foreach ($x in $colecao) { if ($x.Name -like $padrao) { return $x } }; return $null }

if ($Etapa -in 'superficies', 'todas') {
    foreach ($n in 'TN', 'TN_limpo', 'TERRAPLENAGEM', 'ACABADA', 'VOLUME_TERRAPLENAGEM') {
        for ($i = $cdoc.Surfaces.Count - 1; $i -ge 0; $i--) { if ($cdoc.Surfaces.Item($i).Name -eq $n) { $cdoc.Surfaces.Remove($n); "removida superficie $n" } }
    }
    foreach ($n in 'TN', 'TN_limpo', 'TERRAPLENAGEM', 'ACABADA') { [void]$cdoc.Surfaces.ImportXML((Join-Path $AQUI "civil3d\sup_$n.xml")) }
    $est = @{ 'TN' = 'Contours 1m and 5m (Background)'; 'TN_limpo' = '_No Display'; 'TERRAPLENAGEM' = 'Contours 1m and 5m (Design)'; 'ACABADA' = 'Border Only' }
    foreach ($x in $cdoc.Surfaces) { if ($est.ContainsKey($x.Name)) { $st = PorNome $cdoc.SurfaceStyles $est[$x.Name]; if ($st) { $x.Style = $st } } }
    "Superficies apos importar: " + (@($cdoc.Surfaces | % { $_.Name }) -join ', ')
    "Estilos de superficie: " + (@($cdoc.SurfaceStyles | % { $_.Name }) -join ' | ')
}

if ($Etapa -in 'imagem', 'todas') {
    $lay = Camada 'IMAGEM-SATELITE' 7
    foreach ($e in @($adoc.ModelSpace)) { if ($e.ObjectName -eq 'AcDbRasterImage' -and $e.Layer -eq 'IMAGEM-SATELITE') { $e.Delete() } }
    $img = Join-Path $AQUI 'civil3d\imagem_sitio_utm23s.jpg'
    $ins = [double[]]@([double]$P.img.x0, [double]$P.img.y0, 0.0)
    $r = $adoc.ModelSpace.AddRaster($img, $ins, 1.0, 0.0)
    $r.Layer = 'IMAGEM-SATELITE'
    $r.ImageWidth = [double]$P.img.w * [double]$P.img.res
    $r.ImageHeight = [double]$P.img.h * [double]$P.img.res
    $r.Origin = $ins
    "Imagem inserida: {0} x {1} m, origem ({2}, {3})" -f $r.ImageWidth, $r.ImageHeight, $r.Origin[0], $r.Origin[1]
}

if ($Etapa -in 'alinhamento', 'todas') {
    $NOME = 'EIXO PPD 06-24'
    $CAM = Camada 'EIXO-PPD' 1
    for ($i = $cdoc.AlignmentsSiteless.Count - 1; $i -ge 0; $i--) { $a = $cdoc.AlignmentsSiteless.Item($i); if ($a.Name -eq $NOME) { $a.Delete(); 'removido alinhamento anterior' } }
    $estilo = PorNome $cdoc.AlignmentStyles '*Proposed*'; if (-not $estilo) { $estilo = $cdoc.AlignmentStyles.Item(0) }
    $rot = PorNome $cdoc.AlignmentLabelStyleSets '*Major Minor*'; if (-not $rot) { $rot = $cdoc.AlignmentLabelStyleSets.Item(0) }
    $al = $cdoc.AlignmentsSiteless.Add($NOME, 'EIXO-PPD', $estilo, $rot)
    $al.Description = 'Eixo da faixa de pista (2020 m): P0 na extremidade SW da faixa; cabeceira 06 em 0+060 (estaca 3) e 24 em 1+960 (estaca 98). Rumo 060 graus.'
    $p1 = [double[]]@([double]$P.P0[0], [double]$P.P0[1], 0.0)
    $p2 = [double[]]@([double]$P.PF[0], [double]$P.PF[1], 0.0)
    [void]$al.Entities.AddFixedLine1($p1, $p2)
    $al.Update()
    "Alinhamento: {0}  L = {1:N3} m" -f $al.Name, $al.Length

    $tn = $null; foreach ($x in $cdoc.Surfaces) { if ($x.Name -eq 'TN') { $tn = $x } }
    # estilos de perfil validos para o COM ficam em LandProfileStyles (ProfileStyles vem vazio no template NCS)
    $pst = PorNome $cdoc.LandProfileStyles '*terreno existente*'; if (-not $pst) { $pst = $cdoc.LandProfileStyles.Item(0) }
    $pdes = PorNome $cdoc.LandProfileStyles 'Design Profile'; if (-not $pdes) { $pdes = $cdoc.LandProfileStyles.Item(0) }
    $pTN = $al.Profiles.AddFromSurface('TN - eixo', 1, $pst, 'TN', [double]$al.StartingStation, [double]$al.EndingStation, 'EIXO-PPD')
    $pG = $al.Profiles.Add('Greide PPD (acabado)', 2, $pdes)
    foreach ($v in $P.pvis) { [void]$pG.PVIs.Add([double]$v[0], [double]$v[1], 1) }
    $ncv = 0
    for ($k = 1; $k -lt $P.pvis.Count - 1; $k++) {
        $L = [double]$P.pvis[$k][2]
        if ($L -gt 0) { $pv = $pG.PVIs.ItemAt([double]$P.pvis[$k][0], [double]$P.pvis[$k][1]); [void]$pG.Entities.AddFreeSymmetricParabolaByPVIAndCurveLength($pv, $L); $ncv++ }
    }
    $pG.Update()
    "Greide: {0} PVIs, {1} curvas verticais" -f $pG.PVIs.Count, $ncv
    $pvs = PorNome $cdoc.ProfileViewStyles '*Major Grids*'; if (-not $pvs) { $pvs = $cdoc.ProfileViewStyles.Item(0) }
    $bds = PorNome $cdoc.ProfileViewBandStyleSets '*EG-FG Elevations and Stations*'; if (-not $bds) { $bds = $cdoc.ProfileViewBandStyleSets.Item(0) }
    $yv = [double]$P.img.y0 - 600.0; $loc = [double[]]@([double]$P.img.x0, $yv, 0.0)
    [void](Camada 'PERFIS' 7)
    $pv = $al.ProfileViews.Add('Perfil longitudinal PPD', 'PERFIS', $loc, $pvs, $bds)
    "Vista de perfil: " + $pv.Name
    "Estilos: perfil TN=" + $pst.Name + " | greide=" + $pdes.Name + " | vista=" + $pvs.Name + " | bandas=" + $bds.Name
}
$adoc.Save()
'salvo'
