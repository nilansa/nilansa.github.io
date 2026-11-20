(() => {
  'use strict';
  const eta = document.getElementById('learning-rate');
  if (!eta) return;
  const avg = a => a.reduce((total, v) => total + v, 0) / a.length;
  const fmt = x => String(Number(x.toFixed(5))).replace('-', '−');
  const targets = [0, 2, 4];
  const initial = [2, 2, 2];
  const errors = predictions => targets.map((y, i) => y - predictions[i]);
  const sse = predictions => errors(predictions).reduce((s, e) => s + e * e, 0);
  function addTree(predictions, leftCount, rate) {
    const r = errors(predictions);
    const left = avg(r.slice(0, leftCount)), right = avg(r.slice(leftCount));
    return predictions.map((x, i) => x + rate * (i < leftCount ? left : right));
  }
  function draw() {
    const rate = Number(eta.value);
    const one = addTree(initial, 1, rate), two = addTree(one, 2, rate);
    document.getElementById('learning-value').textContent = rate.toFixed(2);
    document.getElementById('boost-results').innerHTML = targets.map((y,i) =>
      '<tr><th scope="row">' + i + '</th><td>' + y + '</td><td>2</td><td>' + fmt(one[i]) +
      '</td><td>' + fmt(two[i]) + '</td><td>' + fmt(y-two[i]) + '</td></tr>').join('');
    document.getElementById('boost-score').textContent =
      'Squared error: ' + [initial, one, two].map(p => fmt(sse(p))).join(' → ');
  }
  eta.addEventListener('input', draw);
  draw();
})();
