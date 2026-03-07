type CategoryInflationValues = {
  monthly_spend_gbp: number;
  inflation_bps: number;
};

export type CategoryInflationMap = Record<string, CategoryInflationValues>;

type CategoryInflationEditorProps = {
  premiumUnlocked: boolean;
  enabled: boolean;
  value: CategoryInflationMap;
  ariaDescribedBy?: string;
  onEnabledChange: (enabled: boolean) => void;
  onChange: (next: CategoryInflationMap) => void;
};

const categories = ["food", "energy", "housing", "transport"] as const;

type CategoryKey = (typeof categories)[number];

function titleCase(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function getCategoryValue(
  map: CategoryInflationMap,
  category: CategoryKey
): CategoryInflationValues {
  return map[category] ?? { monthly_spend_gbp: 0, inflation_bps: 0 };
}

export function CategoryInflationEditor({
  premiumUnlocked,
  enabled,
  value,
  ariaDescribedBy,
  onEnabledChange,
  onChange
}: CategoryInflationEditorProps) {
  if (!premiumUnlocked) {
    return (
      <section className="result-card" aria-label="Category inflation locked">
        <h3>Category inflation (Premium)</h3>
        <p>Premium unlock required to split essentials into category-level inflation assumptions.</p>
      </section>
    );
  }

  return (
    <section className="result-card" aria-label="Category inflation editor">
      <h3>Category inflation (Premium)</h3>
      <label htmlFor="toggle-category-inflation">
        <input
          id="toggle-category-inflation"
          type="checkbox"
          checked={enabled}
          aria-describedby={ariaDescribedBy}
          onChange={(event) => onEnabledChange(event.target.checked)}
        />
        Use category inflation
      </label>

      {enabled ? (
        <div>
          <p>Enter monthly spend and inflation stress per category.</p>
          {categories.map((category) => {
            const categoryValue = getCategoryValue(value, category);
            const label = titleCase(category);

            return (
              <fieldset key={category}>
                <legend>{label}</legend>
                <label htmlFor={`${category}-monthly-spend`}>
                  {label} monthly spend (GBP)
                  <input
                    id={`${category}-monthly-spend`}
                    type="number"
                    min={0}
                    step="0.01"
                    aria-describedby={ariaDescribedBy}
                    value={categoryValue.monthly_spend_gbp}
                    onChange={(event) => {
                      const next = Number(event.target.value);
                      if (!Number.isFinite(next)) {
                        return;
                      }

                      onChange({
                        ...value,
                        [category]: {
                          ...categoryValue,
                          monthly_spend_gbp: next
                        }
                      });
                    }}
                  />
                </label>
                <label htmlFor={`${category}-inflation-bps`}>
                  {label} inflation (bps)
                  <input
                    id={`${category}-inflation-bps`}
                    type="number"
                    min={0}
                    max={10000}
                    step={1}
                    aria-describedby={ariaDescribedBy}
                    value={categoryValue.inflation_bps}
                    onChange={(event) => {
                      const next = Number(event.target.value);
                      if (!Number.isFinite(next)) {
                        return;
                      }

                      onChange({
                        ...value,
                        [category]: {
                          ...categoryValue,
                          inflation_bps: next
                        }
                      });
                    }}
                  />
                </label>
              </fieldset>
            );
          })}
        </div>
      ) : null}
    </section>
  );
}
