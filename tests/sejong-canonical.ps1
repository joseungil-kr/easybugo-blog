param([Parameter(Mandatory)][string]$BuildDir)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $BuildDir).Path
[xml]$sitemap = Get-Content -LiteralPath (Join-Path $root 'sitemap.xml') -Raw -Encoding utf8
$locations = @($sitemap.urlset.url | ForEach-Object { [Uri]::UnescapeDataString($_.loc) })
$duplicates = @()
foreach ($label in @('장례식장', '봉안시설')) {
    $parent = "/$label/세종특별자치시/"
    $duplicate = "${parent}세종특별자치시/"
    $duplicates += $duplicate
    $canonical = "https://blog.easybugo.com$parent"
    foreach ($path in @($parent, $duplicate)) {
        $file = Join-Path $root ($path.Trim('/') + '/index.html')
        $html = [Uri]::UnescapeDataString([IO.File]::ReadAllText($file))
        if ($html -notmatch ('<link rel="?canonical"? href="?' + [regex]::Escape($canonical) + '[">]')) {
            throw "Incorrect canonical: $path"
        }
        if ($html -notmatch ('<meta property="?og:url"? content="?' + [regex]::Escape($canonical) + '[">]')) {
            throw "Incorrect og:url: $path"
        }
        if ($html.Contains('noindex')) { throw "Unexpected noindex: $path" }
    }
    if ($canonical -notin $locations) { throw "Representative URL missing from sitemap: $parent" }
    if ("https://blog.easybugo.com$duplicate" -in $locations) { throw "Duplicate in sitemap: $duplicate" }
}
foreach ($file in Get-ChildItem -LiteralPath $root -Filter '*.html' -Recurse) {
    $html = [Uri]::UnescapeDataString([IO.File]::ReadAllText($file.FullName))
    foreach ($duplicate in $duplicates) {
        if ($html -match ('<a\b[^>]*href="?(?:https://blog\.easybugo\.com)?' + [regex]::Escape($duplicate) + '[">]')) {
            throw "Internal link to duplicate in $($file.FullName)"
        }
    }
}
Write-Output "PASS: both duplicate pairs retain HTML, use representative canonical/og:url, and have no sitemap entries or internal links. Sitemap URLs: $($locations.Count)."
