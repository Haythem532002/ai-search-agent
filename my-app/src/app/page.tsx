"use client";

import { useState } from "react";
import styles from "./page.module.css";

type AgentResponse = {
  topic: string;
  summary: string;
  sources: string[];
  tools_used?: string[];
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AgentResponse | null>(null);

  async function submit(e?: React.FormEvent) {
    e?.preventDefault();
    setError(null);
    setResult(null);

    if (!query.trim()) {
      setError("Please enter a question or topic.");
      return;
    }

    setLoading(true);
    try {
      const encoded = encodeURIComponent(query.trim());
      const res = await fetch(
        `http://localhost:5001/research?query=${encoded}`
      );
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();

      if (data && data.topic && data.summary) {
        const normalized: AgentResponse = {
          topic: data.topic,
          summary: data.summary,
          sources: Array.isArray(data.sources) ? data.sources : [],
          tools_used: Array.isArray(data.tools_used)
            ? data.tools_used
            : undefined,
        };
        setResult(normalized);
      } else {
        setError("Unexpected response shape from server.");
      }
    } catch (err: any) {
      setError(err?.message || String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        {/* Header Section */}
        <header className={styles.header}>
          <div className={styles.logo}>
            <div className={styles.logoIcon}>
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 2L13.09 8.26L20 9L14.55 13.47L16.18 20L12 16.77L7.82 20L9.45 13.47L4 9L10.91 8.26L12 2Z"
                  fill="currentColor"
                  stroke="currentColor"
                  strokeWidth="1.5"
                />
              </svg>
            </div>
            <h1 className={styles.title}>AI Search Agent</h1>
          </div>
          <p className={styles.subtitle}>
            Intelligent research assistant that finds and summarizes information
            from reliable sources
          </p>
        </header>

        {/* Search Form */}
        <form className={styles.form} onSubmit={submit}>
          <div className={styles.inputContainer}>
            <svg className={styles.searchIcon} viewBox="0 0 24 24" fill="none">
              <path
                d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <input
              className={styles.input}
              placeholder="Ask anything — e.g. 'What is the capital of Tunisia?' or 'Explain quantum computing'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={loading}
            />
            {query && (
              <button
                type="button"
                className={styles.clearButton}
                onClick={() => setQuery("")}
              >
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M18 6L6 18M6 6l12 12"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                </svg>
              </button>
            )}
          </div>
          <button className={styles.button} type="submit" disabled={loading}>
            {loading ? (
              <>
                <div className={styles.spinner}></div>
                Searching...
              </>
            ) : (
              <>
                <svg
                  className={styles.buttonIcon}
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <path
                    d="M21 21L15.803 15.803M15.803 15.803C17.209 14.397 18 12.489 18 10.5C18 6.357 14.643 3 10.5 3C6.357 3 3 6.357 3 10.5C3 14.643 6.357 18 10.5 18C12.489 18 14.397 17.209 15.803 15.803Z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                Search
              </>
            )}
          </button>
        </form>

        {/* Error State */}
        {error && (
          <div className={styles.error}>
            <svg className={styles.errorIcon} viewBox="0 0 24 24" fill="none">
              <path
                d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            {error}
          </div>
        )}

        {/* Results Section */}
        {result && (
          <section className={styles.resultCard}>
            <div className={styles.resultHeader}>
              <div className={styles.topicSection}>
                <h2 className={styles.topicTitle}>{result.topic}</h2>
                {result.tools_used && result.tools_used.length > 0 && (
                  <div className={styles.toolsSection}>
                    <span className={styles.toolsLabel}>Tools used:</span>
                    <div className={styles.toolsUsed}>
                      {result.tools_used.map((tool, index) => (
                        <span key={tool} className={styles.toolBadge}>
                          <svg
                            className={styles.toolIcon}
                            viewBox="0 0 24 24"
                            fill="none"
                          >
                            <path
                              d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                            />
                          </svg>
                          {tool}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className={styles.summarySection}>
              <h3 className={styles.summaryTitle}>Summary</h3>
              <p className={styles.summary}>{result.summary}</p>
            </div>

            {result.sources.length > 0 && (
              <div className={styles.sourcesSection}>
                <h3 className={styles.sourcesTitle}>
                  <svg
                    className={styles.sourcesIcon}
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m5.658-5.656a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  Sources
                </h3>
                <div className={styles.sourcesGrid}>
                  {result.sources.map((source, index) => (
                    <a
                      key={source}
                      href={source}
                      target="_blank"
                      rel="noreferrer"
                      className={styles.sourceCard}
                    >
                      <span className={styles.sourceNumber}>{index + 1}</span>
                      <div className={styles.sourceContent}>
                        <span className={styles.sourceUrl}>{source}</span>
                        <svg
                          className={styles.externalIcon}
                          viewBox="0 0 24 24"
                          fill="none"
                        >
                          <path
                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {/* Footer */}
        <footer className={styles.footer}>
          <div className={styles.footerContent}>
            <svg className={styles.footerIcon} viewBox="0 0 24 24" fill="none">
              <path
                d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <span>Powered by local AI Search Agent API</span>
          </div>
        </footer>
      </main>
    </div>
  );
}
