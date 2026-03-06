import { ReactNode } from "react";

type WizardStepProps = {
  id: string;
  title: string;
  children: ReactNode;
};

export function WizardStep({ id, title, children }: WizardStepProps) {
  return (
    <section id={id} className="wizard-step" aria-label={title}>
      <h2>{title}</h2>
      <div className="wizard-step-content">{children}</div>
    </section>
  );
}
