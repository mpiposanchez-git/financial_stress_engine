type GlossaryTooltipProps = {
  term: string;
  definition: string;
};

export function GlossaryTooltip({ term, definition }: GlossaryTooltipProps) {
  return (
    <abbr className="glossary-term" title={definition}>
      {term}
    </abbr>
  );
}
