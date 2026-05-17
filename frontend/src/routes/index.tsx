import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AlertTriangle, RefreshCw, RotateCcw, Save, Train } from "lucide-react";
import type { BoardConfig } from "@/lib/board";
import { DEFAULT_CONFIG } from "@/lib/board";
import { getBoard, getConfig, mockBoardData, resetConfig, saveConfig } from "@/lib/api";
import { TrainSelector } from "@/components/TrainSelector";
import { StationSelector } from "@/components/StationSelector";
import { DirectionSelector } from "@/components/DirectionSelector";
import { BrightnessControl } from "@/components/BrightnessControl";
import { DisplayModeSelector } from "@/components/DisplayModeSelector";
import { BoardPreview } from "@/components/BoardPreview";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Ian's Subway Board — Control Panel" },
      { name: "description", content: "Mobile control panel for a WiFi-connected NYC subway LED arrival board." },
      { property: "og:title", content: "Ian's Subway Board — Control Panel" },
      { property: "og:description", content: "Mobile control panel for a WiFi-connected NYC subway LED arrival board." },
    ],
  }),
  component: Index,
});

type Status =
  | { kind: "connecting" }
  | { kind: "connected"; lastUpdated: number }
  | { kind: "offline" };

function Index() {
  const [config, setConfig] = useState<BoardConfig>(DEFAULT_CONFIG);
  const [status, setStatus] = useState<Status>({ kind: "connecting" });
  const [saving, setSaving] = useState(false);
  const [savedFlash, setSavedFlash] = useState(false);
  const [boardData, setBoardData] = useState(() => mockBoardData(DEFAULT_CONFIG));
  const [tick, setTick] = useState(0); // re-renders for "Xs ago"

  // Load config on mount
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const remote = await getConfig();
        if (cancelled) return;
        setConfig(remote);
        setStatus({ kind: "connected", lastUpdated: Date.now() });
        try {
          const b = await getBoard();
          if (!cancelled) setBoardData(b);
        } catch {
          if (!cancelled) setBoardData(mockBoardData(remote));
        }
      } catch {
        if (!cancelled) setStatus({ kind: "offline" });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Live local preview as config changes (when no fresh remote data)
  const lastRemoteRef = useRef<number>(0);
  useEffect(() => {
    if (Date.now() - lastRemoteRef.current > 2000) {
      setBoardData(mockBoardData(config));
    }
  }, [config]);

  // Tick every second for "last updated"
  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const updateConfig = useCallback(<K extends keyof BoardConfig>(key: K, value: BoardConfig[K]) => {
    setConfig((c) => ({ ...c, [key]: value }));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await saveConfig(config);
      setStatus({ kind: "connected", lastUpdated: Date.now() });
      setSavedFlash(true);
      setTimeout(() => setSavedFlash(false), 1600);
    } catch {
      setStatus({ kind: "offline" });
    } finally {
      setSaving(false);
    }
  };

  const handleRefresh = async () => {
    try {
      const b = await getBoard();
      setBoardData(b);
      lastRemoteRef.current = Date.now();
      setStatus({ kind: "connected", lastUpdated: Date.now() });
    } catch {
      setBoardData(mockBoardData(config));
      setStatus({ kind: "offline" });
    }
  };

  const handleReset = async () => {
    setConfig(DEFAULT_CONFIG);
    setBoardData(mockBoardData(DEFAULT_CONFIG));
    lastRemoteRef.current = 0;

    try {
      const c = await resetConfig();
      setConfig(c);
      setBoardData(mockBoardData(c));
      setStatus({ kind: "connected", lastUpdated: Date.now() });
    } catch {
      setConfig(DEFAULT_CONFIG);
      setBoardData(mockBoardData(DEFAULT_CONFIG));
      setStatus({ kind: "offline" });
    }
  };

  const statusText = useMemo(() => {
    if (status.kind === "connecting") return "Connecting…";
    if (status.kind === "offline") return "Offline";
    const seconds = Math.max(0, Math.floor((Date.now() - status.lastUpdated) / 1000));
    return `Last updated ${seconds}s ago`;
    // tick triggers re-render
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [status, tick]);

  const statusColor =
    status.kind === "connected"
      ? "var(--led-green)"
      : status.kind === "offline"
      ? "var(--destructive)"
      : "var(--led-amber)";

  return (
    <div className="min-h-screen grid-bg pb-32">
      {/* Header */}
      <header className="sticky top-0 z-20 border-b border-border/60 bg-background/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-md items-center justify-between px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="grid size-9 place-items-center rounded-lg border border-primary/40 bg-primary/10 text-primary ring-glow">
              <Train className="size-5" />
            </div>
            <div>
              <h1 className="text-base font-bold leading-tight tracking-tight text-foreground">
                Ian&apos;s Subway Board
              </h1>
              <div className="mt-0.5 flex items-center gap-1.5">
                <span
                  className="pulse-dot block size-1.5 rounded-full"
                  style={{ backgroundColor: statusColor, color: statusColor }}
                />
                <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                  {status.kind === "connected" ? "Connected" : status.kind === "offline" ? "Offline" : "Connecting"}
                  <span className="ml-1 text-muted-foreground/60">· {statusText}</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-md space-y-4 px-4 pt-4">
        {status.kind === "offline" && (
          <div className="flex items-start gap-2 rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive">
            <AlertTriangle className="mt-0.5 size-3.5 shrink-0" />
            <span>Using local preview mode — backend not reachable.</span>
          </div>
        )}

        {/* Preview */}
        <Section>
          <BoardPreview data={boardData} />
        </Section>

        {/* Trains */}
        <Section title="Trains" hint={`${config.trains.length} selected`}>
          <TrainSelector
            selected={config.trains}
            onChange={(v) => updateConfig("trains", v)}
          />
        </Section>

        {/* Stations */}
        <Section title="Stations">
          <StationSelector
            selected={config.stations}
            onChange={(v) => updateConfig("stations", v)}
          />
        </Section>

        {/* Direction */}
        <Section title="Direction">
          <DirectionSelector
            value={config.direction}
            onChange={(v) => updateConfig("direction", v)}
          />
        </Section>

        {/* Brightness */}
        <Section>
          <BrightnessControl
            value={config.brightness}
            onChange={(v) => updateConfig("brightness", v)}
          />
        </Section>

        {/* Display mode */}
        <Section title="Display Mode">
          <DisplayModeSelector
            value={config.mode}
            onChange={(v) => updateConfig("mode", v)}
          />
        </Section>

      </main>

      {/* Sticky action bar */}
      <div className="fixed inset-x-0 bottom-0 z-30 border-t border-border/60 bg-background/85 backdrop-blur-xl">
        <div className="mx-auto max-w-md space-y-2 px-4 py-3">
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={handleRefresh}
              className="flex items-center justify-center gap-2 rounded-xl border border-border bg-secondary/60 py-2.5 text-sm font-medium text-foreground active:scale-[0.98]"
            >
              <RefreshCw className="size-4" />
              Refresh
            </button>
            <button
              onClick={handleReset}
              className="flex items-center justify-center gap-2 rounded-xl border border-destructive/40 py-2.5 text-sm font-medium text-destructive active:scale-[0.98]"
            >
              <RotateCcw className="size-4" />
              Reset
            </button>
          </div>
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex w-full items-center justify-center gap-2 rounded-xl py-3.5 text-sm font-bold uppercase tracking-wider transition-all active:scale-[0.98] disabled:opacity-60"
            style={{
              backgroundColor: savedFlash ? "var(--led-green)" : "var(--primary)",
              color: "var(--primary-foreground)",
              boxShadow: "0 0 24px -6px var(--primary), 0 0 0 1px color-mix(in oklab, var(--primary) 40%, transparent)",
            }}
          >
            <Save className="size-4" />
            {savedFlash ? "Saved to Board" : saving ? "Saving…" : "Save to Board"}
          </button>
        </div>
      </div>
    </div>
  );
}

function Section({
  title,
  hint,
  children,
}: {
  title?: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-border/70 bg-card/60 p-4 backdrop-blur-sm">
      {title && (
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="font-mono text-xs uppercase tracking-[0.18em] text-muted-foreground">
            {title}
          </h2>
          {hint && (
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/70">
              {hint}
            </span>
          )}
        </div>
      )}
      {children}
    </section>
  );
}
