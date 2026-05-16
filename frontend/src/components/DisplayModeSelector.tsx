import type { DisplayMode } from "@/lib/board";
import { Radio, Grid3x3, Clock, Power } from "lucide-react";

interface Props {
  value: DisplayMode;
  onChange: (next: DisplayMode) => void;
}

const MODES: { value: DisplayMode; label: string; Icon: typeof Radio }[] = [
  { value: "arrivals", label: "Arrivals", Icon: Radio },
  { value: "clock_arrivals", label: "Clock + Arrivals", Icon: Clock },
  { value: "test_pattern", label: "Test Pattern", Icon: Grid3x3 },
  { value: "off", label: "Off", Icon: Power },
];

export function DisplayModeSelector({ value, onChange }: Props) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {MODES.map(({ value: v, label, Icon }) => {
        const active = value === v;
        const isOff = v === "off";
        const accent = isOff ? "var(--destructive)" : "var(--accent)";
        return (
          <button
            key={v}
            type="button"
            onClick={() => onChange(v)}
            className="flex items-center gap-3 rounded-xl border px-4 py-3 text-left transition-all active:scale-[0.98]"
            style={{
              borderColor: active ? accent : "var(--border)",
              backgroundColor: active
                ? `color-mix(in oklab, ${accent} 12%, transparent)`
                : "transparent",
              color: active ? accent : "var(--muted-foreground)",
              boxShadow: active ? `0 0 18px -6px ${accent}` : "none",
            }}
            aria-pressed={active}
          >
            <Icon className="size-4 shrink-0" />
            <span className="text-sm font-semibold">{label}</span>
          </button>
        );
      })}
    </div>
  );
}
