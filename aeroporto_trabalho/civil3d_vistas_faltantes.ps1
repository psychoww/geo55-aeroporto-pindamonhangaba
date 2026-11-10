# Cria as vistas de secao que faltam (linhas de amostragem sem vista), sem apagar nada.
# Usado em 09/11 porque civil3d_vistas_secoes.ps1 passou a falhar ("Parametro incorreto") em todas as vistas,
# enquanto este laco, sem $ErrorActionPreference = Stop e sem a etapa de apagar, funciona. Rodar na pasta aeroporto_trabalho.
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$civ = $acad.GetInterfaceObject('AeccXUiLand.AeccApplication.13.9'); $cdoc = $civ.ActiveDocument; $adoc = $acad.ActiveDocument
$P = Get-Content -Raw -Encoding UTF8 'civil3d\projeto.json' | ConvertFrom-Json
$al = $cdoc.AlignmentsSiteless.Item('EIXO PPD 06-24'); $slg = $al.SampleLineGroups.Item('SL - PPD')
$sty = $cdoc.SectionViewStyles.Item('Road Section'); "exagero: " + $sty.GraphStyle.VerticalExaggeration
$bds = $null; foreach ($b in $cdoc.SectionViewBandStyleSets) { if ($b.Name -eq 'Offsets Only') { $bds = $b } }
$n = 0; foreach ($e in $adoc.ModelSpace) { if ($e.ObjectName -eq 'AeccDbGraphCrossSection') { $n++ } }; "vistas no desenho: $n"
$falhas = 0
for ($i = 0; $i -lt $slg.SampleLines.Count; $i++) {
  $sl = $slg.SampleLines.Item($i); if ($sl.SectionViews.Count -gt 0) { continue }
  $loc = [double[]]@(([double]$P.img.x0 + ($i % 6) * 480.0), ([double]$P.img.y0 - 1400.0 - [Math]::Floor($i / 6) * 340.0), 0.0)
  try { [void]$sl.SectionViews.Add('Secao ' + $sl.Name, 'VISTAS-SECOES', $loc, $sty, $bds);  } catch { $falhas++; "erro $i : " + $_.Exception.Message + " | vistas da linha: " + $sl.SectionViews.Count }
}
"falhas: $falhas"; $adoc.Save(); "salvo"
