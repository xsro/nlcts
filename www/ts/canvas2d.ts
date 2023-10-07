import { randomColor1, sci } from "./utils.js";
import chroma from "chroma-js";
import { Data } from "./Data";
import katex from "katex";

export type Elements = {
  canvas: HTMLCanvasElement;
  span_t: HTMLSpanElement;
  span_left_bottom: HTMLSpanElement;
  span_right_top: HTMLSpanElement;
};

export class Canvas2DRender {
  constructor(public eles: Elements) {}
  private colors: { [id: string]: string } = {};
  private color_gen(ids: string[]) {
    const cb = function () {
      if (typeof chroma === "undefined") {
        return randomColor1();
      } else {
        return chroma.random().hex() as string;
      }
    };
    const colors: { [id: string]: string } = this.colors;
    for (const id of ids) {
      if (!colors[id]) colors[id] = cb();
    }
    this.colors = colors;
  }
  private draw_uav(
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    color: string
  ) {
    const pos1 = [
      [1, 1],
      [-1, -1],
    ];
    const pos2 = [
      [1, -1],
      [-1, 1],
    ];
    const delta = this._params.d / 2;
    const radius = this._params.d - Math.sqrt(2) * delta;

    for (const pos of [pos1, pos2]) {
      const x1 = x + pos[0][0] * delta;
      const y1 = y + pos[0][1] * delta;
      const x2 = x + pos[1][0] * delta;
      const y2 = y + pos[1][1] * delta;
      //render uav frame
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
      //render uav rotor
      for (const [x_, y_] of [
        [x1, y1],
        [x2, y2],
      ]) {
        ctx.strokeStyle = "black";
        ctx.fillStyle = color;
        this.drawCircle(ctx, x_, y_, radius);
      }
      ctx.strokeStyle = "gray";
      this.drawCircle(ctx, x, y, this._params.d, false);
    }
  }
  private render_agent(ctx: CanvasRenderingContext2D, px: Data) {
    this.color_gen(Object.keys(px[0].position));
    const t_len = px.length;
    const i_t = t_len - 1;
    for (const [agent, { x, y }] of Object.entries(px[i_t].position)) {
      //final position
      if (agent == "target") {
        ctx.strokeStyle = "red";
        this.drawCircle(ctx, x, y, 8.0, false);
      } else {
        this.draw_uav(ctx, x, y, this.colors[agent]);
      }

      //trajectory
      ctx.beginPath();
      const traj = px.map((ts) => ts.position[agent]);
      ctx.moveTo(traj[0].x, traj[0].y);
      for (const { x, y } of traj.slice(1)) {
        ctx.lineTo(x, y);
      }
      if (typeof chroma !== "undefined") {
        let c = chroma(this.colors[agent]).brighten(0.5).hex();
        ctx.strokeStyle = c;
      }
      ctx.stroke();
    }
  }
  private drawCircle(
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    r: number,
    fill = true
  ) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0.0, 2.0 * Math.PI);
    ctx.closePath();
    if (fill) {
      ctx.fill();
    }
    ctx.stroke();
  }
  public params: { d: number; mu: number } = { d: 1, mu: 3 };
  public _params: { d: number; mu: number } = { d: 1, mu: 3 };
  public render(_data: Data, t_display: number) {
    const canvas = this.eles.canvas;
    // const t0 = this.getElement(".t0") as HTMLInputElement;
    // const t0c = new Function(`const t_final=${t_end};return ${t0.value}`);
    // const t_start = t0c() as number;
    if (_data) {
      const data = structuredClone(_data) as Data;
      let info = {
        xmin: Infinity,
        xmax: -Infinity,
        ymin: Infinity,
        ymax: -Infinity,
      };
      for (const { position } of data) {
        for (const { x, y } of Object.values(position)) {
          if (x < info.xmin) info.xmin = x;
          if (x > info.xmax) info.xmax = x;
          if (y < info.ymin) info.ymin = y;
          if (y > info.ymax) info.ymax = y;
        }
      }

      let center = {
        x: (info.xmax + info.xmin) / 2,
        y: (info.ymax + info.ymin) / 2,
      };
      let m =
        Math.max(
          info.xmax - center.x,
          center.x - info.xmin,
          info.ymax - center.y,
          center.y - info.ymin
        ) *
          2 +
        this.params.d * 2;
      let range = {
        x: (m * 4) / 3,
        y: m * 1,
      };

      const t_expr = "t=" + sci(t_display, 2);
      katex.render(t_expr, this.eles.span_t);

      const rt = this.eles.span_right_top;
      const xmax = center.x + 0.5 * range.x;
      const ymax = center.y + 0.5 * range.y;
      const rt_expr = sci(xmax, 2) + "," + sci(ymax, 2);
      katex.render(rt_expr, rt);

      const lb = this.eles.span_left_bottom;
      const xmin = center.x - 0.5 * range.x;
      const ymin = center.y - 0.5 * range.y;
      const lb_expr = sci(xmin, 2) + "," + sci(ymin, 2);
      katex.render(lb_expr, lb, {});

      const map_to_px = (pos: { x: number; y: number }) => {
        return {
          x: canvas.width / 2 + (pos.x - center.x) * (canvas.width / range.x),
          y: canvas.height / 2 - (pos.y - center.y) * (canvas.height / range.y),
        };
      };
      for (const { position } of data) {
        for (const agent in position) {
          let pos = position[agent];
          position[agent] = map_to_px(pos);
        }
      }

      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.clearRect(0.0, 0.0, canvas.width, canvas.height);

        this._params.d = (this.params.d * (0.5 * canvas.height)) / range.x;
        this._params.mu = (this.params.mu * (0.5 * canvas.height)) / range.y;

        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.moveTo(canvas.width - 1 - this._params.mu, canvas.height - 6);
        ctx.lineTo(canvas.width - 1, canvas.height - 6);
        ctx.stroke();
        ctx.fillStyle = "green";
        const sz = 3;

        this.drawCircle(ctx, canvas.width - 1, canvas.height - 6, sz);
        this.drawCircle(
          ctx,
          canvas.width - 1 - this._params.mu,
          canvas.height - 6,
          sz
        );
        this.drawCircle(
          ctx,
          canvas.width - 1 - this._params.d,
          canvas.height - 6,
          sz
        );
        this.render_agent(ctx, data);
      }
    }
  }
}
