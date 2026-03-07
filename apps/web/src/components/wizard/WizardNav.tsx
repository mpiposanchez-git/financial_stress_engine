type WizardNavProps = {
  currentStep: number;
  totalSteps: number;
  onBack: () => void;
  onNext: () => void;
  isSubmitting: boolean;
};

export function WizardNav({ currentStep, totalSteps, onBack, onNext, isSubmitting }: WizardNavProps) {
  const isFirst = currentStep === 0;
  const isLast = currentStep === totalSteps - 1;

  return (
    <div className="wizard-nav">
      <button type="button" onClick={onBack} disabled={isFirst}>
        Back
      </button>
      {isLast ? (
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Running…" : "Run simulation"}
        </button>
      ) : (
        <button type="button" onClick={onNext}>
          Next
        </button>
      )}
    </div>
  );
}
