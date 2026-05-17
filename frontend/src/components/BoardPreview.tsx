import { useEffect, useState } from "react";
import type { BoardData } from "@/lib/board";
import { trainColorVar, trainTextOnColor } from "@/lib/board";

interface Props {
  data: BoardData;
}

export function BoardPreview({ data }: Props) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const dim = Math.max(0.9, data.brightness / 100);

  if (data.mode === "off") {
    return (
      <Shell>
        <div className="grid h-full place-items-center">
          <div className="font-mono text-xs uppercase tracking-[0.3em] text-muted-foreground/40">
            — board off —
          </div>
        </div>
      </Shell>
    );
  }

  if (data.mode === "test_pattern") {
    return (
      <Shell>
        <div className="grid h-full grid-cols-8 gap-px p-2">
          {Array.from({ length: 32 }).map((_, i) => {
            const colors = ["var(--led-red)", "var(--led-green)", "var(--led-amber)", "var(--primary)"];
            return (
              <div
                key={i}
                className="rounded-sm"
                style={{
                  backgroundColor: colors[i % colors.length],
                  opacity: dim,
                }}
              />
            );
          })}
        </div>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="flex h-full flex-col gap-1.5 p-3" style={{ opacity: dim }}>
        {data.mode === "clock_arrivals" && (
          <div className="mb-1 flex items-center justify-between border-b border-white/5 pb-1">
            <span className="font-mono text-[10px] uppercase tracking-widest text-glow-amber" style={{ color: "var(--led-amber)" }}>
              MTA
            </span>
            <span className="font-mono text-sm tabular-nums text-glow-amber" style={{ color: "var(--led-amber)" }}>
              {now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false })}
            </span>
          </div>
        )}

        {data.stations.length === 0 && (
          <div className="grid flex-1 place-items-center font-mono text-[10px] uppercase tracking-widest text-muted-foreground/50">
            no stations selected
          </div>
        )}

        {data.stations.slice(0, 2).map((st) => (
          <div key={st.name} className="space-y-0.5">
            <div
              className="truncate font-mono text-[11px] font-bold uppercase tracking-wider text-glow-amber"
              style={{ color: "var(--led-amber)" }}
            >
              {st.name}
            </div>
            <div className="flex flex-wrap gap-x-2 gap-y-0.5 font-mono text-[11px]">
              {st.arrivals.length === 0 && (
                <span className="text-muted-foreground/50">— no service —</span>
              )}
              {st.arrivals.map((a, idx) => (
                <span key={idx} className="inline-flex items-center gap-1">
                  <span
                    className="grid size-4 place-items-center rounded-full text-[9px] font-bold leading-none"
                    style={{
                      backgroundColor: trainColorVar(a.route),
                      color: trainTextOnColor(a.route),
                      boxShadow: `0 0 6px -1px ${trainColorVar(a.route)}`,
                    }}
                  >
                    {a.route}
                  </span>
                  <span style={{ color: "var(--led-green)" }} className="text-glow-amber">
                    {a.direction === "uptown" ? "↑" : "↓"}
                  </span>
                  <span style={{ color: "var(--led-amber)" }} className="text-glow-amber tabular-nums">
                    {a.minutes}m
                  </span>
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Shell>
  );
}

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div
      className="relative aspect-[2/1] w-full overflow-hidden rounded-xl border border-white/10"
      style={{ backgroundColor: "var(--led-bg)" }}
    >
      {/* matrix dot pattern */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage:
            "radial-gradient(circle, color-mix(in oklab, white 8%, transparent) 0.5px, transparent 1px)",
          backgroundSize: "6px 6px",
        }}
      />
      <div className="relative h-full">{children}</div>
      <div className="pointer-events-none absolute inset-0 scanlines opacity-40" />
      <div
        className="pointer-events-none absolute inset-0 rounded-xl"
        style={{ boxShadow: "inset 0 0 40px rgba(0,0,0,0.7)" }}
      />
    </div>
  );
}
