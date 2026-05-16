interface Props {
  value: number;
  onChange: (next: number) => void;
}

const PRESETS = [
  { label: "Night", val: 10 },
  { label: "Normal", val: 25 },
  { label: "Bright", val: 75 },
];

export function BrightnessControl({ value, onChange }: Props) {
  return (
    <div className="space-y-4">
      <div className="flex items-baseline justify-between">
        <span className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
          Brightness
        </span>
        <span className="font-mono text-2xl font-bold text-primary text-glow-cyan">
          {value}
          <span className="text-sm text-muted-foreground">%</span>
        </span>
      </div>

      <input
        type="range"
        min={5}
        max={100}
        step={1}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="h-2 w-full cursor-pointer appearance-none rounded-full bg-secondary accent-[var(--primary)]"
        style={{
          background: `linear-gradient(to right, var(--primary) 0%, var(--primary) ${((value - 5) / 95) * 100}%, var(--secondary) ${((value - 5) / 95) * 100}%, var(--secondary) 100%)`,
        }}
      />

      <div className="grid grid-cols-3 gap-2">
        {PRESETS.map((p) => {
          const active = value === p.val;
          return (
            <button
              key={p.label}
              type="button"
              onClick={() => onChange(p.val)}
              className="rounded-lg border py-2 font-mono text-xs uppercase tracking-wider transition-all active:scale-95"
              style={{
                borderColor: active ? "var(--primary)" : "var(--border)",
                color: active ? "var(--primary)" : "var(--muted-foreground)",
                backgroundColor: active
                  ? "color-mix(in oklab, var(--primary) 12%, transparent)"
                  : "transparent",
              }}
            >
              {p.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
