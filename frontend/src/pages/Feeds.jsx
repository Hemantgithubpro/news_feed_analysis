import React, { useState, useEffect } from "react";
import { getFeeds, addFeed, deleteFeed, refreshFeed } from "../api";

const Feeds = () => {
  const [feeds, setFeeds] = useState([]);
  const [newUrl, setNewUrl] = useState("");
  const [newName, setNewName] = useState("");

  useEffect(() => {
    loadFeeds();
  }, []);

  const loadFeeds = async () => {
    try {
      const res = await getFeeds();
      setFeeds(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await addFeed(newUrl, newName);
      setNewUrl("");
      setNewName("");
      loadFeeds();
    } catch (e) {
      alert("Failed to add feed");
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure?")) return;
    try {
      await deleteFeed(id);
      loadFeeds();
    } catch (e) {
      alert("Error deleting feed");
    }
  };

  const handleRefresh = async (id) => {
    try {
      await refreshFeed(id);
      alert("Refresh scheduled");
    } catch (e) {
      alert("Error refreshing feed");
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Manage RSS Feeds</h1>

      <div className="bg-white p-6 rounded shadow mb-8">
        <h2 className="text-lg font-semibold mb-4">Add New Feed</h2>
        <form onSubmit={handleAdd} className="flex gap-4">
          <input
            type="text"
            placeholder="Feed Name (e.g. TechCrunch)"
            className="border p-2 rounded flex-1"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            required
          />
          <input
            type="url"
            placeholder="RSS URL"
            className="border p-2 rounded flex-2 w-1/2"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            required
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Add Feed
          </button>
        </form>
      </div>

      <div className="bg-white rounded shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                URL
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {feeds.map((feed) => (
              <tr key={feed.id}>
                <td className="px-6 py-4 whitespace-nowrap">{feed.name}</td>
                <td className="px-6 py-4 truncate max-w-xs">{feed.url}</td>
                <td className="px-6 py-4">
                  {feed.error_count > 0 ? (
                    <span className="text-red-500">
                      Error ({feed.error_count})
                    </span>
                  ) : (
                    <span className="text-green-500">Active</span>
                  )}
                </td>
                <td className="px-6 py-4 text-right space-x-2">
                  <button
                    onClick={() => handleRefresh(feed.id)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    Refresh
                  </button>
                  <button
                    onClick={() => handleDelete(feed.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Feeds;
