# Exporta a geometria (links) das seções TN_limpo e "Corredor PPD - Datum" de todas as linhas do SL - PPD.
# Saída: civil3d/secoes_corredor.csv (estaca, fonte, x1, z1, x2, z2). Áreas e volumes: corredor_volumes.py
$ErrorActionPreference = 'Stop'
$AQUI = $PSScriptRoot
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$civ = $acad.GetInterfaceObject('AeccXUiLand.AeccApplication.13.9')
$slg = $civ.ActiveDocument.AlignmentsSiteless.Item('EIXO PPD 06-24').SampleLineGroups.Item(0)
$out = New-Object System.Collections.Generic.List[string]
$out.Add('estaca,fonte,x1,z1,x2,z2')
$inv = [Globalization.CultureInfo]::InvariantCulture
for ($i = 0; $i -lt $slg.SampleLines.Count; $i++) {
    $l = $slg.SampleLines.Item($i)
    for ($j = 0; $j -lt $l.Sections.Count; $j++) {
        $s = $l.Sections.Item($j)
        $fonte = $null
        if ($s.Name -like '* - TN_limpo(*') { $fonte = 'TN_limpo' } elseif ($s.Name -like '* - Corredor PPD - Datum(*') { $fonte = 'Datum' }
        if (-not $fonte) { continue }
        if ($s.StaticDynamic -ne 0) { $s.StaticDynamic = 0; $s.Update() }
        $st = $l.Station
        for ($k = 0; $k -lt $s.Links.Count; $k++) {
            $lk = $s.Links.Item($k)
            $out.Add([string]::Format($inv, '{0:F3},{1},{2:F4},{3:F4},{4:F4},{5:F4}', $st, $fonte, $lk.StartPointX, $lk.StartPointY, $lk.EndPointX, $lk.EndPointY))
        }
    }
}
[IO.File]::WriteAllLines((Join-Path $AQUI 'civil3d\secoes_corredor.csv'), $out)
"linhas: $($slg.SampleLines.Count)  links exportados: $($out.Count - 1)"
