import { useMemo, useState } from "react";
import { Search, X } from "lucide-react";
import { MAX_STATIONS, STATIONS } from "@/lib/board";

interface Props {
  selected: string[];
  onChange: (next: string[]) => void;
}

export function StationSelector({ selected, onChange }: Props) {
  const [query, setQuery] = useState("");
  const matches = useMemo(() => {
    const q = query.trim().toLowerCase();
    return STATIONS.filter(
      (s) => !selected.includes(s) && (q === "" || s.toLowerCase().includes(q)),
    );
  }, [query, selected]);

  const add = (name: string) => {
    if (selected.length >= MAX_STATIONS) return;
    onChange([...selected, name]);
    setQuery("");
  };
  const remove = (name: string) =>
    onChange(selected.filter((s) => s !== name));

  const atMax = selected.length >= MAX_STATIONS;

  return (
    <div className="space-y-3">
      <div className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          inputMode="search"
          placeholder={atMax ? `Max ${MAX_STATIONS} stations` : "Search stations…"}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={atMax}
          className="w-full rounded-xl border border-border bg-input/60 py-3 pl-10 pr-3 text-base text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-50"
        />
      </div>

      {!atMax && matches.length > 0 && (
        <ul className="overflow-hidden rounded-xl border border-border bg-card/60">
          {matches.map((s) => (
            <li key={s}>
              <button
                type="button"
                onClick={() => add(s)}
                className="block w-full px-4 py-3 text-left text-sm text-foreground transition-colors hover:bg-secondary active:bg-secondary"
              >
                {s}
              </button>
            </li>
          ))}
        </ul>
      )}

      {selected.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selected.map((s) => (
            <span
              key={s}
              className="inline-flex items-center gap-2 rounded-full border border-primary/40 bg-primary/10 px-3 py-1.5 text-sm text-primary"
            >
              {s}
              <button
                type="button"
                onClick={() => remove(s)}
                className="grid size-4 place-items-center rounded-full text-primary/80 hover:text-primary"
                aria-label={`Remove ${s}`}
              >
                <X className="size-3.5" />
              </button>
            </span>
          ))}
        </div>
      )}

      <p className="font-mono text-xs text-muted-foreground">
        {selected.length}/{MAX_STATIONS} selected
      </p>
    </div>
  );
}
