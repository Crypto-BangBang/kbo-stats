/* Stadium seating map drawer — canvas-based, per-stadium configs */

const STADIUM_CONFIGS = {
  jamsil: {
    name: "잠실야구장",
    colors: { premium: "#c8960c", inner1: "#1a4fa0", inner2: "#2d6ed6", cheer: "#276749", outer: "#1e5e38" },
    rings: [
      { label: "테이블석",   r1: 78,  r2: 100, start: 40,  end: 140, count: 6,  prefix: "T",  color: "#c8960c" },
      { label: "내야1층",    r1: 102, r2: 148, start: 30,  end: 150, count: 14, prefix: "1",  color: "#1a4fa0" },
      { label: "내야2층",    r1: 150, r2: 190, start: 22,  end: 158, count: 12, prefix: "2",  color: "#2d6ed6" },
      { label: "외야응원석", r1: 192, r2: 225, start: 10,  end: 170, count: 8,  prefix: "3",  color: "#276749" },
      { label: "외야일반석", r1: 226, r2: 252, start: 355, end: 185, count: 8,  prefix: "4",  color: "#1e5e38", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  gocheok: {
    name: "고척스카이돔",
    colors: { premium: "#c8960c", inner1: "#cc5500", inner2: "#e07030", outer: "#884400" },
    rings: [
      { label: "테이블석", r1: 80,  r2: 105, start: 50,  end: 130, count: 5,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 107, r2: 155, start: 10,  end: 170, count: 14, prefix: "1", color: "#cc5500" },
      { label: "내야2층",  r1: 157, r2: 200, start: 5,   end: 175, count: 14, prefix: "2", color: "#e07030" },
      { label: "외야석",   r1: 202, r2: 248, start: 350, end: 190, count: 16, prefix: "3", color: "#884400", wrap: true },
    ],
    dome: true,
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  suwon: {
    name: "수원KT위즈파크",
    colors: { premium: "#c8960c", inner1: "#8b0000", inner2: "#c0392b", outer: "#5e0000" },
    rings: [
      { label: "테이블석", r1: 78,  r2: 100, start: 45,  end: 135, count: 5,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 102, r2: 148, start: 32,  end: 148, count: 12, prefix: "1", color: "#8b0000" },
      { label: "내야2층",  r1: 150, r2: 192, start: 22,  end: 158, count: 10, prefix: "2", color: "#c0392b" },
      { label: "외야석",   r1: 194, r2: 240, start: 355, end: 185, count: 10, prefix: "3", color: "#5e0000", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  incheon: {
    name: "인천SSG랜더스필드",
    colors: { premium: "#c8960c", inner1: "#0047ab", inner2: "#1565c0", outer: "#003080" },
    rings: [
      { label: "테이블석", r1: 78,  r2: 100, start: 42,  end: 138, count: 5,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 102, r2: 150, start: 28,  end: 152, count: 13, prefix: "1", color: "#0047ab" },
      { label: "내야2층",  r1: 152, r2: 195, start: 20,  end: 160, count: 11, prefix: "2", color: "#1565c0" },
      { label: "외야석",   r1: 197, r2: 242, start: 358, end: 182, count: 10, prefix: "3", color: "#003080", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  daegu: {
    name: "대구삼성라이온즈파크",
    colors: { premium: "#c8960c", inner1: "#003087", inner2: "#1565c0", outer: "#001a4d" },
    rings: [
      { label: "VIP석",   r1: 78,  r2: 100, start: 45,  end: 135, count: 4,  prefix: "V", color: "#c8960c" },
      { label: "내야1층", r1: 102, r2: 150, start: 30,  end: 150, count: 13, prefix: "1", color: "#003087" },
      { label: "내야2층", r1: 152, r2: 198, start: 20,  end: 160, count: 12, prefix: "2", color: "#1565c0" },
      { label: "외야석",  r1: 200, r2: 248, start: 355, end: 185, count: 10, prefix: "3", color: "#001a4d", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  busan: {
    name: "부산사직야구장",
    colors: { premium: "#c8960c", inner1: "#1a237e", inner2: "#283593", outer: "#0d1459" },
    rings: [
      { label: "테이블석", r1: 78,  r2: 100, start: 42,  end: 138, count: 5,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 102, r2: 148, start: 30,  end: 150, count: 13, prefix: "1", color: "#1a237e" },
      { label: "내야2층",  r1: 150, r2: 195, start: 22,  end: 158, count: 11, prefix: "2", color: "#283593" },
      { label: "외야석",   r1: 197, r2: 242, start: 356, end: 184, count: 10, prefix: "3", color: "#0d1459", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  gwangju: {
    name: "광주-기아챔피언스필드",
    colors: { premium: "#c8960c", inner1: "#006400", inner2: "#228b22", outer: "#004000" },
    rings: [
      { label: "테이블석", r1: 78,  r2: 100, start: 44,  end: 136, count: 5,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 102, r2: 148, start: 30,  end: 150, count: 12, prefix: "1", color: "#006400" },
      { label: "내야2층",  r1: 150, r2: 195, start: 22,  end: 158, count: 10, prefix: "2", color: "#228b22" },
      { label: "외야석",   r1: 197, r2: 240, start: 356, end: 184, count: 10, prefix: "3", color: "#004000", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  daejeon: {
    name: "한화생명이글스파크",
    colors: { premium: "#c8960c", inner1: "#e55a00", inner2: "#ff7020", outer: "#a04000" },
    rings: [
      { label: "테이블석", r1: 72,  r2: 92,  start: 46,  end: 134, count: 4,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 94,  r2: 138, start: 32,  end: 148, count: 11, prefix: "1", color: "#e55a00" },
      { label: "내야2층",  r1: 140, r2: 178, start: 22,  end: 158, count: 9,  prefix: "2", color: "#ff7020" },
      { label: "외야석",   r1: 180, r2: 220, start: 356, end: 184, count: 8,  prefix: "3", color: "#a04000", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  changwon: {
    name: "창원NC파크",
    colors: { premium: "#c8960c", inner1: "#00008b", inner2: "#0000cd", outer: "#000060" },
    rings: [
      { label: "테이블석", r1: 78,  r2: 100, start: 44,  end: 136, count: 5,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 102, r2: 150, start: 30,  end: 150, count: 13, prefix: "1", color: "#00008b" },
      { label: "내야2층",  r1: 152, r2: 196, start: 22,  end: 158, count: 11, prefix: "2", color: "#0000cd" },
      { label: "외야석",   r1: 198, r2: 244, start: 355, end: 185, count: 10, prefix: "3", color: "#000060", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  },
  ulsan: {
    name: "울산문수야구장",
    colors: { premium: "#c8960c", inner1: "#4b0082", inner2: "#7b2fbe", outer: "#2e0050" },
    rings: [
      { label: "테이블석", r1: 68,  r2: 88,  start: 46,  end: 134, count: 4,  prefix: "T", color: "#c8960c" },
      { label: "내야1층",  r1: 90,  r2: 132, start: 32,  end: 148, count: 10, prefix: "1", color: "#4b0082" },
      { label: "내야2층",  r1: 134, r2: 170, start: 22,  end: 158, count: 8,  prefix: "2", color: "#7b2fbe" },
      { label: "외야석",   r1: 172, r2: 210, start: 356, end: 184, count: 8,  prefix: "3", color: "#2e0050", wrap: true },
    ],
    field: { warning: "#b5651d", grass: "#2d6a4f", dirt: "#c4a265" }
  }
};

const DEG = Math.PI / 180;

function toRad(deg) { return deg * DEG; }

/*
 * Canvas coordinate system:
 *  - home plate = bottom center
 *  - center field = top center
 *  - 0° = right (3시), angles go clockwise
 *  - We want home plate angle = 90° (bottom), so:
 *    - 1루쪽 = right side = angles near 0° (converted to canvas: 270+angle)
 *    - Actually easier: define our own angle system
 *      stadium_angle=0 => right field line (1루)
 *      stadium_angle=90 => center field (top)
 *      stadium_angle=180 => left field line (3루)
 *    - Canvas angles: stadium_angle 0..180 maps to canvas_angle 0..-180 (counterclockwise from right)
 *    - i.e. canvas_angle = -stadium_angle * DEG (but canvas arc is clockwise)
 *    - We draw arcs from (180-start)° to (180-end)° in canvas coords
 */

function drawField(ctx, cx, cy, cfg) {
  const f = cfg.field;

  // outfield grass
  ctx.beginPath();
  ctx.arc(cx, cy, 215, Math.PI, 2 * Math.PI);
  ctx.fillStyle = f.grass;
  ctx.fill();

  // foul territory fill
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.arc(cx, cy, 215, Math.PI, 2 * Math.PI);
  ctx.closePath();
  ctx.fillStyle = f.grass;
  ctx.fill();

  // warning track arc
  ctx.beginPath();
  ctx.arc(cx, cy, 195, Math.PI, 2 * Math.PI);
  ctx.fillStyle = f.warning;
  ctx.fill();

  // inner grass
  ctx.beginPath();
  ctx.arc(cx, cy, 178, Math.PI, 2 * Math.PI);
  ctx.fillStyle = f.grass;
  ctx.fill();

  // infield dirt diamond area (ellipse)
  ctx.beginPath();
  ctx.ellipse(cx, cy - 28, 88, 68, 0, 0, 2 * Math.PI);
  ctx.fillStyle = f.dirt;
  ctx.fill();

  // infield grass (rotated square)
  ctx.save();
  ctx.translate(cx, cy - 28);
  ctx.rotate(45 * DEG);
  ctx.fillStyle = f.grass;
  ctx.fillRect(-46, -46, 92, 92);
  ctx.restore();

  // pitcher's mound
  ctx.beginPath();
  ctx.ellipse(cx, cy - 28, 11, 9, 0, 0, 2 * Math.PI);
  ctx.fillStyle = f.dirt;
  ctx.fill();

  // bases
  const bsize = 7;
  function drawBase(bx, by) {
    ctx.save();
    ctx.translate(bx, by);
    ctx.rotate(45 * DEG);
    ctx.fillStyle = "white";
    ctx.fillRect(-bsize/2, -bsize/2, bsize, bsize);
    ctx.restore();
  }
  drawBase(cx, cy - 28 - 56);      // 2루
  drawBase(cx + 56, cy - 28);      // 1루
  drawBase(cx - 56, cy - 28);      // 3루

  // home plate
  ctx.beginPath();
  ctx.moveTo(cx, cy + 8);
  ctx.lineTo(cx - 8, cy + 2);
  ctx.lineTo(cx - 8, cy - 5);
  ctx.lineTo(cx + 8, cy - 5);
  ctx.lineTo(cx + 8, cy + 2);
  ctx.closePath();
  ctx.fillStyle = "white";
  ctx.fill();

  // foul lines
  ctx.strokeStyle = "rgba(255,255,255,0.7)";
  ctx.lineWidth = 1.5;
  ctx.setLineDash([5, 4]);
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx - 200, cy - 200);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + 200, cy - 200);
  ctx.stroke();
  ctx.setLineDash([]);
}

function drawRing(ctx, cx, cy, ring, isDome) {
  const startRad = (180 - ring.start) * DEG;
  const endRad   = (180 - ring.end)   * DEG;
  const totalArc = ring.wrap
    ? ((ring.start - ring.end + 360) % 360) * DEG
    : (ring.start - ring.end) * DEG;
  const perSection = totalArc / ring.count;
  const baseNum = ring.prefix === "T" ? 0 : ring.prefix === "V" ? 0 : parseInt(ring.prefix) * 100;

  for (let i = 0; i < ring.count; i++) {
    const aStart = startRad - i * perSection;
    const aEnd   = aStart - perSection;
    const aMid   = (aStart + aEnd) / 2;

    // sector fill
    ctx.beginPath();
    ctx.arc(cx, cy, ring.r2, aStart, aEnd, true);
    ctx.arc(cx, cy, ring.r1, aEnd, aStart, false);
    ctx.closePath();
    ctx.fillStyle = ring.color;
    ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.25)";
    ctx.lineWidth = 0.8;
    ctx.stroke();

    // section number label
    const labelR = (ring.r1 + ring.r2) / 2;
    const lx = cx + labelR * Math.cos(aMid);
    const ly = cy + labelR * Math.sin(aMid);
    const sectionNum = ring.prefix === "T" || ring.prefix === "V"
      ? `${ring.prefix}${i + 1}`
      : `${parseInt(ring.prefix) * 100 + i + 1}`;

    ctx.save();
    ctx.translate(lx, ly);
    const rot = aMid > Math.PI / 2 && aMid < 3 * Math.PI / 2 ? aMid - Math.PI : aMid;
    ctx.rotate(rot);
    ctx.fillStyle = "rgba(255,255,255,0.92)";
    ctx.font = `bold ${ring.r2 - ring.r1 > 35 ? 9 : 7}px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(sectionNum, 0, 0);
    ctx.restore();
  }
}

function drawDomeCeiling(ctx, cx, cy, r) {
  const grad = ctx.createRadialGradient(cx, cy - 60, 30, cx, cy - 60, r + 30);
  grad.addColorStop(0, "rgba(60,60,90,0.0)");
  grad.addColorStop(1, "rgba(30,30,60,0.55)");
  ctx.beginPath();
  ctx.arc(cx, cy, r + 30, 0, 2 * Math.PI);
  ctx.fillStyle = grad;
  ctx.fill();

  // dome ring
  ctx.beginPath();
  ctx.arc(cx, cy, r + 20, 0, 2 * Math.PI);
  ctx.strokeStyle = "rgba(180,180,220,0.4)";
  ctx.lineWidth = 6;
  ctx.stroke();
}

function drawCompass(ctx, cx, cy) {
  ctx.fillStyle = "rgba(180,180,180,0.7)";
  ctx.font = "10px sans-serif";
  ctx.textAlign = "center";
}

function drawLegend(ctx, cfg, canvasW, canvasH) {
  const items = cfg.rings.slice().reverse();
  const x = 10, startY = canvasH - 10 - items.length * 18;
  ctx.font = "10px sans-serif";
  items.forEach((ring, i) => {
    const y = startY + i * 18;
    ctx.fillStyle = ring.color;
    ctx.fillRect(x, y - 7, 14, 12);
    ctx.strokeStyle = "rgba(255,255,255,0.4)";
    ctx.lineWidth = 0.5;
    ctx.strokeRect(x, y - 7, 14, 12);
    ctx.fillStyle = "#ccc";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(ring.label, x + 18, y);
  });
}

function drawStadiumMap(canvasId, stadiumId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const cfg = STADIUM_CONFIGS[stadiumId];
  if (!cfg) return;

  const W = canvas.width  = canvas.offsetWidth  || 600;
  const H = canvas.height = canvas.offsetHeight || 520;
  const ctx = canvas.getContext("2d");

  // background
  ctx.fillStyle = "#12182a";
  ctx.fillRect(0, 0, W, H);

  const cx = W / 2;
  const cy = H * 0.58; // home plate position

  // Draw seating rings (outermost first)
  const rings = cfg.rings.slice().reverse();
  rings.forEach(ring => drawRing(ctx, cx, cy, ring, cfg.dome));

  // Draw baseball field on top
  drawField(ctx, cx, cy, cfg);

  // Dome overlay
  if (cfg.dome) {
    const outerR = Math.max(...cfg.rings.map(r => r.r2));
    drawDomeCeiling(ctx, cx, cy, outerR);
  }

  // Labels: outfield, 1루, 3루
  ctx.fillStyle = "rgba(200,200,200,0.8)";
  ctx.font = "11px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("↑ 외야", cx, 18);
  ctx.fillText("홈플레이트 ↓", cx, H - 6);

  ctx.save();
  ctx.translate(18, cy);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("3루", 0, 0);
  ctx.restore();

  ctx.save();
  ctx.translate(W - 18, cy);
  ctx.rotate(Math.PI / 2);
  ctx.fillText("1루", 0, 0);
  ctx.restore();

  // Legend
  drawLegend(ctx, cfg, W, H);

  // Stadium name watermark
  ctx.fillStyle = "rgba(255,255,255,0.06)";
  ctx.font = "bold 28px sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(cfg.name, cx, cy - 160);
}

window.StadiumMap = { draw: drawStadiumMap };
