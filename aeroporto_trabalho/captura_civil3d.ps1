# Zoom numa janela (coordenadas do desenho) e captura da janela do Civil 3D em PNG.
param([double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [string]$Saida)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W { [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
public struct RECT { public int L, T, R, B; } }
"@
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject('AutoCAD.Application')
$acad.WindowState = 3
$h = [IntPtr]$acad.HWND
[W]::ShowWindow($h, 3) | Out-Null; [W]::SetForegroundWindow($h) | Out-Null; Start-Sleep -Milliseconds 800
$c = [Globalization.CultureInfo]::InvariantCulture
$cmd = '_.ZOOM _W ' + $X1.ToString($c) + ',' + $Y1.ToString($c) + ' ' + $X2.ToString($c) + ',' + $Y2.ToString($c) + ' '
$acad.ActiveDocument.SendCommand($cmd)
Start-Sleep -Milliseconds 2500
$r = New-Object W+RECT; [W]::GetWindowRect($h, [ref]$r) | Out-Null
$bmp = New-Object Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
$g = [Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
$bmp.Save($Saida, [Drawing.Imaging.ImageFormat]::Png); "captura: $Saida ($($bmp.Width)x$($bmp.Height))"
