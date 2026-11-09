# Extrai do Civil 3D as seções TN_limpo e TERRAPLENAGEM de todas as linhas de amostragem (ElevationAt a cada 0,25 m)
# Saída: civil3d\secoes_civil3d.csv (estaca;offset;z_tn_limpo;z_terraplenagem)
$ErrorActionPreference = 'Stop'
$inv = [Globalization.CultureInfo]::InvariantCulture
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$civ = $acad.GetInterfaceObject('AeccXUiLand.AeccApplication.13.9'); $cdoc = $civ.ActiveDocument
$al = $cdoc.AlignmentsSiteless.Item('EIXO PPD 06-24'); $slg = $al.SampleLineGroups.Item('SL - PPD')
$offs = New-Object System.Collections.Generic.List[double]
for ($k = 0; $k -le 1600; $k++) { $offs.Add($k * 0.25 - 200.0) }
foreach ($b in 22.5, 22.52, 30.0, 30.02) { $offs.Add($b); $offs.Add(-$b) }
$offs = $offs | Sort-Object -Unique
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('estaca;offset;z_tn_limpo;z_terraplenagem;dl_esq;dl_dir')
for ($i = 0; $i -lt $slg.SampleLines.Count; $i++) {
    $sl = $slg.SampleLines.Item($i)
    if ($null -eq $sl.Station -or "$($sl.Station)" -eq '') { "linha $i sem estaca ({0}) - ignorada" -f $sl.Name; continue }
    $secLimpo = $null; $secTerr = $null
    for ($j = 0; $j -lt $sl.Sections.Count; $j++) {
        $s = $sl.Sections.Item($j); $s.StaticDynamic = 0; $s.Update()
        if ($s.Surface.Name -eq 'TN_limpo') { $secLimpo = $s } elseif ($s.Surface.Name -eq 'TERRAPLENAGEM') { $secTerr = $s }
    }
    $dle = $secTerr.LengthLeft; $dld = $secTerr.LengthRight
    if ($null -eq $dle -or $null -eq $dld -or "$dle" -eq '') { "secao vazia na estaca {0} (borda da superficie)" -f $sl.Station; $dle = 0.0; $dld = 0.0 }
    $dle = [double]$dle; $dld = [double]$dld
    foreach ($o in $offs) {
        $zl = ''; $zt = ''
        try { $zl = $secLimpo.ElevationAt($o).ToString('F4', $inv) } catch {}
        if ($o -ge $dle -and $o -le $dld) { try { $zt = $secTerr.ElevationAt($o).ToString('F4', $inv) } catch {} }
        [void]$sb.AppendLine(('{0};{1};{2};{3};{4};{5}' -f $sl.Station.ToString('F3', $inv), $o.ToString('F2', $inv), $zl, $zt, $dle.ToString('F3', $inv), $dld.ToString('F3', $inv)))
    }
}
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'civil3d\secoes_civil3d.csv'), $sb.ToString())
"linhas de amostragem exportadas: " + $slg.SampleLines.Count
