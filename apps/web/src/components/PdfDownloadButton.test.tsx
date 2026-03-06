import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { PdfDownloadButton } from "./PdfDownloadButton";

describe("PdfDownloadButton", () => {
  it("calls onDownload when clicked", () => {
    const onDownload = vi.fn().mockResolvedValue(undefined);

    render(<PdfDownloadButton onDownload={onDownload} loading={false} />);

    fireEvent.click(screen.getByRole("button", { name: "Download PDF report" }));
    expect(onDownload).toHaveBeenCalledTimes(1);
  });
});
