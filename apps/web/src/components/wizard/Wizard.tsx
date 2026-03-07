import { ReactNode } from "react";

type WizardProps = {
  currentStep: number;
  totalSteps: number;
  title: string;
  children: ReactNode;
};

export function Wizard({ currentStep, totalSteps, title, children }: WizardProps) {
  return (
    <section className="wizard-shell" aria-live="polite">
      <p className="wizard-progress">
        Step {currentStep + 1} of {totalSteps}
      </p>
      <div>{children}</div>
      <p className="wizard-step-label">Current step: {title}</p>
    </section>
  );
}
