type PercentSliderValueKind = "percent" | "bps";

type PercentSliderProps = {
  id: string;
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
  ariaDescribedBy?: string;
  valueKind?: PercentSliderValueKind;
};

function toPercentAndBps(value: number, valueKind: PercentSliderValueKind): { percent: number; bps: number } {
  if (valueKind === "bps") {
    return { percent: value / 100, bps: value };
  }

  return { percent: value, bps: value * 100 };
}

export function PercentSlider({
  id,
  label,
  value,
  onChange,
  min,
  max,
  step = 0.1,
  ariaDescribedBy,
  valueKind = "percent"
}: PercentSliderProps) {
  const { percent, bps } = toPercentAndBps(value, valueKind);

  return (
    <div className="percent-slider">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        aria-label={label}
        aria-describedby={ariaDescribedBy}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
      />
      <p className="percent-slider-value" aria-live="polite">
        {percent.toFixed(2)}% ({Math.round(bps)} bps)
      </p>
    </div>
  );
}
