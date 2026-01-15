import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Feeds from "./pages/Feeds";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100 font-sans text-gray-900">
        <nav className="bg-white shadow">
          <div className="container mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <span className="font-bold text-xl text-blue-600">
                    NewsIntel
                  </span>
                </div>
                <div className="ml-6 flex space-x-8">
                  <Link
                    to="/"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500 text-gray-500 hover:text-gray-700"
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/feeds"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500 text-gray-500 hover:text-gray-700"
                  >
                    Feeds
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/feeds" element={<Feeds />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
