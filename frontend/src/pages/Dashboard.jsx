import React from "react";
import Stats from "../components/Stats";
import ArticleList from "../components/ArticleList";

const Dashboard = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">
        News Intelligence Dashboard
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <h2 className="text-xl font-bold mb-4">Latest News</h2>
          <ArticleList />
        </div>

        <div className="lg:col-span-1">
          <Stats />

          {/* Placeholder for Word Cloud or other widgets */}
          <div className="bg-white p-4 rounded shadow mt-6">
            <h3 className="font-bold mb-2">System Status</h3>
            <p className="text-sm text-gray-600">
              <strong>Backend:</strong>{" "}
              <span className="text-green-600">Online</span>
            </p>
            <p className="text-sm text-gray-600">
              <strong>Worker:</strong>{" "}
              <span className="text-green-600">Active</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
