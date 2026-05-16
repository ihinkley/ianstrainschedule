import type { Direction } from "@/lib/board";
import { ArrowUp, ArrowDown, ArrowUpDown } from "lucide-react";

interface Props {
  value: Direction;
  onChange: (next: Direction) => void;
}

const OPTIONS: { value: Direction; label: string; sub: string; Icon: typeof ArrowUp }[] = [
  { value: "northbound", label: "Uptown", sub: "Bronx / Queens", Icon: ArrowUp },
  { value: "both", label: "Both", sub: "All directions", Icon: ArrowUpDown },
  { value: "southbound", label: "Downtown", sub: "Brooklyn", Icon: ArrowDown },
];

export function DirectionSelector({ value, onChange }: Props) {
  return (
    <div className="grid grid-cols-3 gap-2">
      {OPTIONS.map(({ value: v, label, sub, Icon }) => {
        const active = value === v;
        return (
          <button
            key={v}
            type="button"
            onClick={() => onChange(v)}
            className="flex flex-col items-center gap-1 rounded-xl border p-3 text-center transition-all active:scale-95"
            style={{
              borderColor: active ? "var(--primary)" : "var(--border)",
              backgroundColor: active ? "color-mix(in oklab, var(--primary) 12%, transparent)" : "transparent",
              color: active ? "var(--primary)" : "var(--muted-foreground)",
              boxShadow: active ? "0 0 18px -6px var(--primary)" : "none",
            }}
            aria-pressed={active}
          >
            <Icon className="size-5" />
            <span className="text-sm font-semibold">{label}</span>
            <span className="font-mono text-[10px] uppercase tracking-wider opacity-70">{sub}</span>
          </button>
        );
      })}
    </div>
  );
}
