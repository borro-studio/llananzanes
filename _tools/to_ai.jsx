// Abre el PDF de la home en Illustrator y lo guarda como .ai nativo
(function(){
  app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
  for (var d = app.documents.length - 1; d >= 0; d--) { if (/^llananzanes-home/.test(app.documents[d].name)) app.documents[d].close(SaveOptions.DONOTSAVECHANGES); }
  var src = new File("~/Downloads/llananzanes/export/_para-ai.pdf");
  var o = app.preferences.PDFFileOptions; o.pageToOpen = 1;
  var doc = app.open(src);
  // Unir en un solo cuadro las palabras de una misma línea (misma fuente, cuerpo, color y línea base)
  (function(){
    var items = [];
    for (var i = 0; i < doc.textFrames.length; i++) {
      var t = doc.textFrames[i];
      try {
        if (t.kind != TextType.POINTTEXT) continue;
        var ca = t.textRange.characterAttributes, c = ca.fillColor, b = t.geometricBounds;
        var col = c.typename == "RGBColor" ? [Math.round(c.red), Math.round(c.green), Math.round(c.blue)].join(",") : c.typename;
        items.push({ t: t, x: t.anchor[0], y: t.anchor[1], r: b[2], size: ca.size, key: ca.textFont.name + "|" + Math.round(ca.size * 10) + "|" + col });
      } catch (e) {}
    }
    items.sort(function (a, b) { return Math.abs(a.y - b.y) > 0.6 ? b.y - a.y : a.x - b.x; });
    var cur = null;
    for (var k = 0; k < items.length; k++) {
      var it = items[k];
      if (cur && it.key == cur.key && Math.abs(it.y - cur.y) <= 0.6 && it.x - cur.r < cur.size * 0.75 && it.x - cur.r > -cur.size * 0.2) {
        var gap = it.x - cur.r;
        cur.t.contents = cur.t.contents + (gap > cur.size * 0.08 ? " " : "") + it.t.contents;
        cur.r = it.r; it.t.remove();
      } else { cur = it; }
    }
  })();
  var fonts = {}, n = doc.textFrames.length;
  var one = 0; for (var i = 0; i < n; i++) { if (doc.textFrames[i].contents.indexOf(" ") < 0) one++; try { fonts[doc.textFrames[i].textRange.characterAttributes.textFont.name] = 1; } catch(e){} }
  var names = []; for (var k in fonts) names.push(k);
  var opt = new IllustratorSaveOptions(); opt.pdfCompatible = true; opt.embedLinkedFiles = true; opt.compressed = true;
  doc.saveAs(new File("~/Downloads/llananzanes/export/llananzanes-home.ai"), opt);
  var res = "textFrames=" + n + " | sinEspacios=" + one + " | placed=" + doc.placedItems.length + " | raster=" + doc.rasterItems.length + " | paths=" + doc.pathItems.length + " | fonts=" + names.join(", ") + " | artboard=" + doc.artboards[0].artboardRect;
  var f = new File("~/Downloads/llananzanes/export/_ai_report.txt"); f.open("w"); f.write(res); f.close();
  return res;
})();
