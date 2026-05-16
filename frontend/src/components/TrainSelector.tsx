import { ALL_TRAINS, trainColorVar, trainTextOnColor } from "@/lib/board";

interface Props {
  selected: string[];
  onChange: (next: string[]) => void;
}

export function TrainSelector({ selected, onChange }: Props) {
  const toggle = (route: string) => {
    onChange(
      selected.includes(route)
        ? selected.filter((r) => r !== route)
        : [...selected, route],
    );
  };

  return (
    <div className="grid grid-cols-6 gap-2">
      {ALL_TRAINS.map((route) => {
        const active = selected.includes(route);
        const bg = trainColorVar(route);
        const fg = trainTextOnColor(route);
        return (
          <button
            key={route}
            type="button"
            onClick={() => toggle(route)}
            className="relative flex aspect-square items-center justify-center rounded-full font-mono text-lg font-bold transition-all active:scale-95"
            style={{
              backgroundColor: active ? bg : "transparent",
              color: active ? fg : "var(--muted-foreground)",
              border: `1.5px solid ${active ? bg : "var(--border)"}`,
              boxShadow: active
                ? `0 0 18px -4px ${bg}, inset 0 0 0 2px color-mix(in oklab, ${bg} 30%, transparent)`
                : "none",
            }}
            aria-pressed={active}
            aria-label={`Train ${route}`}
          >
            {route}
          </button>
        );
      })}
    </div>
  );
}
