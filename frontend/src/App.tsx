import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import TopicPage from "./pages/TopicPage";
import SourcePage from "./pages/SourcePage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/topic/:topic" element={<TopicPage />} />
        <Route path="/source/:source" element={<SourcePage />} />

      </Routes>
    </BrowserRouter>
  );
}
