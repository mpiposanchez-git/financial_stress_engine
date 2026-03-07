type CurrencyCode = "GBP" | "EUR" | "USD";

type CurrencySelectProps = {
  id: string;
  label: string;
  value: CurrencyCode;
  onChange: (value: CurrencyCode) => void;
  currencies?: readonly CurrencyCode[];
  ariaDescribedBy?: string;
};

const defaultCurrencies: readonly CurrencyCode[] = ["GBP", "EUR", "USD"];

export function CurrencySelect({
  id,
  label,
  value,
  onChange,
  currencies = defaultCurrencies,
  ariaDescribedBy
}: CurrencySelectProps) {
  return (
    <label htmlFor={id}>
      {label}
      <select
        id={id}
        aria-label={label}
        aria-describedby={ariaDescribedBy}
        value={value}
        onChange={(event) => onChange(event.target.value as CurrencyCode)}
      >
        {currencies.map((currency) => (
          <option key={currency} value={currency}>
            {currency}
          </option>
        ))}
      </select>
    </label>
  );
}
