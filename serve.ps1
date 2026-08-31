# =====================================================================
# 123MiniApps — tiny local static server (no admin, no Python needed)
# Uses a raw TCP socket bound to loopback, so it never needs a URL
# reservation or administrator rights. Serves the folder this script
# sits in, and opens the browser once it is actually listening.
# =====================================================================

$port = 8000
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$url  = "http://localhost:$port/"

$mime = @{
  '.html'='text/html; charset=utf-8'; '.htm'='text/html; charset=utf-8';
  '.css'='text/css; charset=utf-8';   '.js'='application/javascript; charset=utf-8';
  '.mjs'='application/javascript; charset=utf-8'; '.json'='application/json; charset=utf-8';
  '.svg'='image/svg+xml'; '.png'='image/png'; '.jpg'='image/jpeg'; '.jpeg'='image/jpeg';
  '.gif'='image/gif'; '.webp'='image/webp'; '.ico'='image/x-icon';
  '.woff'='font/woff'; '.woff2'='font/woff2'; '.ttf'='font/ttf';
  '.xml'='application/xml'; '.txt'='text/plain; charset=utf-8';
  '.webmanifest'='application/manifest+json'; '.map'='application/json'
}

$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $port)
try {
  $listener.Start()
} catch {
  Write-Host ""
  Write-Host "  Could not start the server on port $port." -ForegroundColor Yellow
  Write-Host "  It may already be running in another window - try opening $url" -ForegroundColor Yellow
  Write-Host ""
  Start-Process $url
  Read-Host "  Press Enter to close"
  return
}

Write-Host ""
Write-Host "  ===============================================" -ForegroundColor Cyan
Write-Host "     123MiniApps is running" -ForegroundColor Green
Write-Host "  ===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "     Open:    $url"
Write-Host "     Folder:  $root"
Write-Host ""
Write-Host "     Keep this window open while you use the site." -ForegroundColor Gray
Write-Host "     Close it (or press Ctrl+C) to stop the server." -ForegroundColor Gray
Write-Host ""

# The listener is up, so opening the browser now will connect cleanly.
Start-Process $url

while ($true) {
  try {
    $client = $listener.AcceptTcpClient()
  } catch {
    break
  }
  try {
    $client.ReceiveTimeout = 1500
    # Linger on close so the full response is flushed to the browser before the
    # socket shuts down. Without this, large files (CSS/JS) can be truncated,
    # which breaks the page's JavaScript (themes, category tabs, etc.).
    $client.LingerState = New-Object System.Net.Sockets.LingerOption($true, 5)
    $client.NoDelay = $true
    $stream = $client.GetStream()

    # Read the request (we only need the first line: "GET /path HTTP/1.1")
    $buf = New-Object byte[] 8192
    $count = $stream.Read($buf, 0, $buf.Length)
    if ($count -le 0) { $client.Close(); continue }
    $request = [System.Text.Encoding]::ASCII.GetString($buf, 0, $count)
    $firstLine = ($request -split "`r`n")[0]
    $rawPath = ($firstLine -split ' ')[1]
    if (-not $rawPath) { $rawPath = '/' }

    $path = [Uri]::UnescapeDataString(($rawPath -split '\?')[0])
    if ($path -eq '/' -or $path.EndsWith('/')) { $path = $path + 'index.html' }
    $rel = $path.TrimStart('/') -replace '/', '\'
    $file = Join-Path $root $rel

    if ((Test-Path -LiteralPath $file -PathType Leaf)) {
      $bytes = [System.IO.File]::ReadAllBytes($file)
      $ext = [System.IO.Path]::GetExtension($file).ToLower()
      $ct = $mime[$ext]
      if (-not $ct) { $ct = 'application/octet-stream' }
      $head = "HTTP/1.0 200 OK`r`nContent-Type: $ct`r`nContent-Length: $($bytes.Length)`r`nCache-Control: no-cache`r`nConnection: close`r`n`r`n"
      $hb = [System.Text.Encoding]::ASCII.GetBytes($head)
      $stream.Write($hb, 0, $hb.Length)
      $stream.Write($bytes, 0, $bytes.Length)
    } else {
      $body = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $path")
      $head = "HTTP/1.0 404 Not Found`r`nContent-Type: text/plain; charset=utf-8`r`nContent-Length: $($body.Length)`r`nConnection: close`r`n`r`n"
      $hb = [System.Text.Encoding]::ASCII.GetBytes($head)
      $stream.Write($hb, 0, $hb.Length)
      $stream.Write($body, 0, $body.Length)
    }
    $stream.Flush()
    # Signal we are done sending, then close the stream so all bytes are flushed
    # to the client before the socket is torn down.
    try { $client.Client.Shutdown([System.Net.Sockets.SocketShutdown]::Send) } catch {}
    try { $stream.Close() } catch {}
  } catch {
    # ignore a broken/aborted connection and keep serving
  } finally {
    try { $client.Close() } catch {}
  }
}
