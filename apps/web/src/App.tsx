import { HashRouter, Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "./components/ProtectedRoute";
import { AboutPage } from "./pages/AboutPage";
import { DataSourcesPage } from "./pages/DataSourcesPage";
import { HomePage } from "./pages/HomePage";
import { ResultsPage } from "./pages/ResultsPage";
import { StressTestPage } from "./pages/StressTestPage";

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/data-sources" element={<DataSourcesPage />} />
        <Route
          path="/stress-test"
          element={
            <ProtectedRoute>
              <StressTestPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/results"
          element={
            <ProtectedRoute>
              <ResultsPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </HashRouter>
  );
}
