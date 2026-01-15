import React, { useEffect, useState } from "react";
import { getArticles } from "../api";
import { format } from "date-fns";

const ArticleList = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      const response = await getArticles();
      setArticles(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading articles...</div>;

  return (
    <div className="space-y-4">
      {articles.map((article) => (
        <div
          key={article.id}
          className="bg-white p-4 rounded shadow hover:shadow-md transition-shadow"
        >
          <div className="flex justify-between items-start">
            <h3 className="text-lg font-semibold text-blue-600">
              <a href={article.url} target="_blank" rel="noopener noreferrer">
                {article.title}
              </a>
            </h3>
            <span
              className={`px-2 py-1 rounded text-xs font-bold 
                            ${
                              article.analysis?.sentiment_label === "POSITIVE"
                                ? "bg-green-100 text-green-800"
                                : article.analysis?.sentiment_label ===
                                  "NEGATIVE"
                                ? "bg-red-100 text-red-800"
                                : "bg-gray-100 text-gray-800"
                            }`}
            >
              {article.analysis?.sentiment_label || "N/A"}
            </span>
          </div>
          <p className="text-gray-500 text-sm mb-2">
            {format(
              new Date(article.published_at || article.created_at),
              "MMM dd, yyyy HH:mm"
            )}
          </p>

          {article.analysis?.keywords && (
            <div className="flex flex-wrap gap-2 mt-2">
              {article.analysis.keywords.slice(0, 5).map((kw, idx) => (
                <span
                  key={idx}
                  className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs"
                >
                  {kw}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ArticleList;
