function rand(N: number, x: number, y: number, range: number): number[] {
  const res: number[] = [];
  for (let i = 0; i < N; i++) {
    res.push(x + 2 * range * (Math.random() - 0.5));
    res.push(y + 2 * range * (Math.random() - 0.5));
  }
  return res;
}

export function parse(str: string): number[] {
  let r = /rand\(([\d\.-]+),([\d\.-]+),([\d\.-]+),([\d\.-]+)\)/;
  let re = r.exec(str);

  while (re) {
    const N = parseFloat(re[1]);
    const x = parseFloat(re[2]);
    const y = parseFloat(re[3]);
    const range = parseFloat(re[4]);
    const values = rand(N, x, y, range);
    str = str.replace(re[0], values.join(","));
    re = r.exec(str);
  }

  str = str.replace(/\[/g, "").replace(/\]/g, "");
  return str.split(",").map(parseFloat);
}

export function randomColor1(rm = 256, gm = 256, bm = 256) {
  let r = Math.floor(Math.random() * rm);
  let g = Math.floor(Math.random() * gm);
  let b = Math.floor(Math.random() * bm);
  //在控制器中显示出随机生成的颜色(可以删除,无影响)
  console.log("rgb(" + r + "," + g + "," + b + ")");
  //返回随机生成的颜色
  return "rgb(" + r + "," + g + "," + b + ")";
}
export function randomColor2(): string {
  let str1 = "#";
  for (let i = 0; i < 6; i++) {
    str1 += Math.floor(Math.random() * 9);
  }
  //在控制器中显示出随机生成的颜色(可以删除,无影响)
  console.log(str1);
  //返回随机生成的颜色
  return str1;
}

export function sci(a: number, l: number) {
  const idx = Math.log10(Math.abs(a));
  const index = idx > 0 ? Math.floor(idx) : Math.ceil(idx);
  const coeff = a / Math.pow(10, index);
  let expr = `${coeff.toFixed(l)}\\times10^{${index}}`;
  if (index == 0) expr = `${coeff.toFixed(l)}`;
  if (index == 1) expr = `${coeff.toFixed(l)}\\times10`;
  if (index == 1) expr = `${a.toFixed(l)}`;
  return expr;
}

export function down_txt(text: string, filename: string) {
  //Convert JSON Array to string.
  let json = [text];
  //Convert JSON string to BLOB.
  const blob1 = new Blob(json, { type: "text/plain;charset=utf-8" });
  const url = window.URL || window.webkitURL;
  const link = url.createObjectURL(blob1);
  const a = document.createElement("a");
  a.download = filename;
  a.href = link;
  document.body.append(a);
  a.click();
  document.body.removeChild(a);
}
