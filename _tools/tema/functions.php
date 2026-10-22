<?php
/* Sirve las páginas HTML de la carpeta /web del tema según la URL.
   Las direcciones son las mismas que en la web estática: /, /casa-i.html, /experiencias/esqui-y-nieve.html...
   Si los archivos pesados no caben en la subida, se cambia LLN_MEDIA por otra dirección (p. ej. otro servidor). */
if (!defined('LLN_MEDIA')) define('LLN_MEDIA', get_template_directory_uri() . '/web/assets/');

add_action('template_redirect', function () {
    $dir  = get_template_directory() . '/web/';
    $path = trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
    if ($path === '') $path = 'index.html';
    if (substr($path, -5) !== '.html') $path .= '.html';           // /casa-i -> casa-i.html
    $file = realpath($dir . $path);
    if (!$file || strpos($file, realpath($dir)) !== 0) {            // no existe: portada con 404
        status_header(404); $file = $dir . 'index.html';
    } else status_header(200);
    $html = file_get_contents($file);
    $html = str_replace(['"../assets/', '"assets/', "url(assets/", "url(../assets/"],
                        ['"' . LLN_MEDIA, '"' . LLN_MEDIA, 'url(' . LLN_MEDIA, 'url(' . LLN_MEDIA], $html);
    header('Content-Type: text/html; charset=utf-8');
    echo $html;
    exit;
});
