import { DeterministicResponse, InputParameters, MonteCarloResponse, SensitivityDriverImpact } from "../types";

type ExportBundleArgs = {
  inputParameters: InputParameters | null | undefined;
  deterministic: DeterministicResponse;
  montecarlo: MonteCarloResponse | null | undefined;
  sensitivityImpacts: SensitivityDriverImpact[] | null;
  premiumUnlocked: boolean;
  provenance: Record<string, unknown>;
  appVersion: string;
  modelVersion: string;
};

export function formatJsonExportFilename(reportingCurrency: string, date = new Date()): string {
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  return `stress-export-${year}-${month}-${day}-${reportingCurrency}.json`;
}

export function buildExportBundle(args: ExportBundleArgs): Record<string, unknown> {
  return {
    input_payload: args.inputParameters ?? null,
    deterministic_outputs: args.deterministic,
    montecarlo_outputs: args.premiumUnlocked ? (args.montecarlo ?? null) : null,
    sensitivity_outputs: args.premiumUnlocked ? (args.sensitivityImpacts ?? null) : null,
    provenance: args.provenance,
    versions: {
      app_version: args.appVersion,
      model_version: args.modelVersion,
    },
  };
}

export function downloadJsonBundle(bundle: Record<string, unknown>, filename: string): void {
  const content = JSON.stringify(bundle, null, 2);
  const blob = new Blob([content], { type: "application/json" });
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(objectUrl);
}
