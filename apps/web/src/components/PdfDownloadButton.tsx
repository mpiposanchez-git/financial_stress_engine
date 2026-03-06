type PdfDownloadButtonProps = {
  onDownload: () => Promise<void>;
  loading: boolean;
};

export function PdfDownloadButton({ onDownload, loading }: PdfDownloadButtonProps) {
  return (
    <section className="result-card" aria-label="PDF download">
      <h2>PDF report export</h2>
      <button type="button" onClick={() => void onDownload()} disabled={loading}>
        {loading ? "Preparing PDF..." : "Download PDF report"}
      </button>
    </section>
  );
}
