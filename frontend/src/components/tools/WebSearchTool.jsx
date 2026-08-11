
import React, { useState } from 'react';
import { tools } from '../../api/endpoints';

const WebSearchTool = () => {
  // ============================================================
  // SEARCH STATE
  // ============================================================

  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searchedQuery, setSearchedQuery] = useState('');

  // ============================================================
  // GENERAL STATE
  // ============================================================

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // ============================================================
  // WEBPAGE STATE
  // ============================================================

  const [selectedPage, setSelectedPage] = useState(null);
  const [pageLoading, setPageLoading] = useState(false);

  const [summary, setSummary] = useState('');
  const [summaryLoading, setSummaryLoading] = useState(false);

  const [question, setQuestion] = useState('');
  const [pageAnswer, setPageAnswer] = useState('');
  const [answerLoading, setAnswerLoading] = useState(false);

  // ============================================================
  // RESEARCH STATE
  // ============================================================

  const [research, setResearch] = useState(null);
  const [researchLoading, setResearchLoading] = useState(false);

  // ============================================================
  // SEARCH
  // ============================================================

  const performSearch = async () => {
    const cleanQuery = query.trim();

    if (!cleanQuery) {
      setError('Please enter something to search for.');
      return;
    }

    setLoading(true);
    setError('');

    setResults([]);
    setSearchedQuery('');
    setSelectedPage(null);
    setSummary('');
    setPageAnswer('');
    setResearch(null);

    try {
      const response = await tools.web.search(cleanQuery);

      const data = response.data;

      if (!data.success) {
        setError(data.error || 'Web search failed.');
        return;
      }

      setResults(data.results || []);
      setSearchedQuery(data.query || cleanQuery);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Unable to perform web search.'
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // KEYBOARD SEARCH
  // ============================================================

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      performSearch();
    }
  };

  // ============================================================
  // READ WEBPAGE
  // ============================================================

  const readPage = async (url) => {
    if (!url) return;

    setPageLoading(true);
    setError('');
    setSummary('');
    setPageAnswer('');
    setResearch(null);

    try {
      const response = await tools.web.read(url);

      const data = response.data;

      if (!data.success) {
        setError(data.error || 'Unable to read webpage.');
        return;
      }

      setSelectedPage(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Unable to read webpage.'
      );
    } finally {
      setPageLoading(false);
    }
  };

  // ============================================================
  // SUMMARIZE PAGE
  // ============================================================

  const summarizePage = async () => {
    if (!selectedPage?.url) return;

    setSummaryLoading(true);
    setError('');

    try {
      const response = await tools.web.summarize(
        selectedPage.url
      );

      const data = response.data;

      if (!data.success) {
        setError(data.error || 'Unable to summarize webpage.');
        return;
      }

      setSummary(data.summary || '');
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Unable to summarize webpage.'
      );
    } finally {
      setSummaryLoading(false);
    }
  };

  // ============================================================
  // ASK ABOUT PAGE
  // ============================================================

  const askAboutPage = async () => {
    const cleanQuestion = question.trim();

    if (!selectedPage?.url) {
      setError('Read a webpage first.');
      return;
    }

    if (!cleanQuestion) {
      setError('Enter a question first.');
      return;
    }

    setAnswerLoading(true);
    setError('');
    setPageAnswer('');

    try {
      const response = await tools.web.ask(
        selectedPage.url,
        cleanQuestion
      );

      const data = response.data;

      if (!data.success) {
        setError(
          data.error || 'Unable to answer the question.'
        );
        return;
      }

      setPageAnswer(data.answer || '');
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Unable to answer question.'
      );
    } finally {
      setAnswerLoading(false);
    }
  };

  // ============================================================
  // FULL WEB RESEARCH
  // ============================================================

  const performResearch = async () => {
    const cleanQuery = query.trim();

    if (!cleanQuery) {
      setError('Enter a research topic first.');
      return;
    }

    setResearchLoading(true);
    setError('');
    setResearch(null);

    try {
      const response = await tools.web.research(cleanQuery);

      const data = response.data;

      if (!data.success) {
        setError(
          data.error || 'Web research failed.'
        );
        return;
      }

      setResearch(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Unable to perform web research.'
      );
    } finally {
      setResearchLoading(false);
    }
  };

  // ============================================================
  // CLEAR
  // ============================================================

  const clearWorkspace = () => {
    setQuery('');
    setResults([]);
    setSearchedQuery('');
    setSelectedPage(null);
    setSummary('');
    setQuestion('');
    setPageAnswer('');
    setResearch(null);
    setError('');
  };

  // ============================================================
  // RESULT CARD
  // ============================================================

  const renderResult = (result, index) => {
    return (
      <div
        key={`${result.url || 'result'}-${index}`}
        style={{
          padding: '18px',
          borderRadius: '12px',
          border: '1px solid rgba(255,255,255,0.07)',
          background: 'rgba(255,255,255,0.025)',
        }}
      >
        {/* TITLE */}

        <a
          href={result.url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: '#00d4ff',
            fontSize: '16px',
            fontWeight: '600',
            textDecoration: 'none',
          }}
        >
          {result.title || 'Untitled result'}
        </a>

        {/* URL */}

        {result.url && (
          <div
            style={{
              marginTop: '6px',
              marginBottom: '10px',
              color: '#666678',
              fontSize: '11px',
              wordBreak: 'break-all',
            }}
          >
            {result.url}
          </div>
        )}

        {/* SNIPPET */}

        <div
          style={{
            color: '#b5b5c5',
            fontSize: '13px',
            lineHeight: '1.6',
            marginBottom: '14px',
          }}
        >
          {result.snippet ||
            'No description available.'}
        </div>

        {/* ACTIONS */}

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '8px',
          }}
        >
          <button
            type="button"
            onClick={() => readPage(result.url)}
            style={buttonStyle}
          >
            📖 Read
          </button>

          <a
            href={result.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              ...buttonStyle,
              textDecoration: 'none',
              display: 'inline-flex',
              alignItems: 'center',
            }}
          >
            🔗 Open
          </a>
        </div>
      </div>
    );
  };

  // ============================================================
  // MAIN UI
  // ============================================================

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '1100px',
        margin: '0 auto',
        padding: '30px',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.06)',
        background: 'rgba(18,18,26,0.65)',
        boxSizing: 'border-box',
      }}
    >
      {/* ======================================================
          HEADER
      ====================================================== */}

      <div style={{ marginBottom: '24px' }}>
        <div
          style={{
            fontSize: '42px',
            marginBottom: '8px',
          }}
        >
          🌐
        </div>

        <h2
          style={{
            margin: 0,
            color: '#ffffff',
            fontSize: '22px',
          }}
        >
          Web Research
        </h2>

        <p
          style={{
            margin: '6px 0 0',
            color: '#77778a',
            fontSize: '13px',
          }}
        >
          Search the web, read pages, summarize information,
          ask questions and research topics with PhantomAI.
        </p>
      </div>

      {/* ======================================================
          SEARCH BAR
      ====================================================== */}

      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '8px',
          marginBottom: '12px',
        }}
      >
        <input
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Search or research something..."
          style={{
            flex: 1,
            minWidth: '220px',
            padding: '13px 14px',
            borderRadius: '9px',
            border:
              '1px solid rgba(255,255,255,0.08)',
            background: '#0c0c12',
            color: '#ffffff',
            outline: 'none',
            boxSizing: 'border-box',
          }}
        />

        <button
          type="button"
          onClick={performSearch}
          disabled={loading || researchLoading}
          style={primaryButtonStyle}
        >
          {loading ? 'Searching...' : '🔍 Search'}
        </button>

        <button
          type="button"
          onClick={performResearch}
          disabled={researchLoading || loading}
          style={researchButtonStyle}
        >
          {researchLoading
            ? 'Researching...'
            : '🧠 Research'}
        </button>

        <button
          type="button"
          onClick={clearWorkspace}
          style={secondaryButtonStyle}
        >
          Clear
        </button>
      </div>

      {/* ======================================================
          ERROR
      ====================================================== */}

      {error && (
        <div
          style={{
            marginBottom: '18px',
            padding: '13px',
            borderRadius: '9px',
            background: 'rgba(255,70,70,0.08)',
            border:
              '1px solid rgba(255,70,70,0.2)',
            color: '#ff8b8b',
            fontSize: '13px',
          }}
        >
          {error}
        </div>
      )}

      {/* ======================================================
          SEARCHED QUERY
      ====================================================== */}

      {searchedQuery && !loading && (
        <div
          style={{
            marginBottom: '18px',
            color: '#888899',
            fontSize: '13px',
          }}
        >
          Search results for:{' '}
          <strong style={{ color: '#ffffff' }}>
            {searchedQuery}
          </strong>
        </div>
      )}

      {/* ======================================================
          RESEARCH RESULT
      ====================================================== */}

      {research && (
        <div
          style={{
            marginBottom: '25px',
            padding: '22px',
            borderRadius: '13px',
            border:
              '1px solid rgba(0,212,255,0.18)',
            background:
              'rgba(0,212,255,0.035)',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '10px',
              marginBottom: '15px',
            }}
          >
            <h3
              style={{
                margin: 0,
                color: '#ffffff',
                fontSize: '18px',
              }}
            >
              🧠 PhantomAI Research
            </h3>

            <span
              style={{
                color: '#77778a',
                fontSize: '11px',
              }}
            >
              {research.source_count || 0} sources
            </span>
          </div>

          <div
            style={{
              color: '#d0d0d8',
              fontSize: '14px',
              lineHeight: '1.75',
              whiteSpace: 'pre-wrap',
            }}
          >
            {research.answer ||
              'No research answer returned.'}
          </div>

          {/* SOURCES */}

          {research.sources?.length > 0 && (
            <div style={{ marginTop: '22px' }}>
              <h4
                style={{
                  margin: '0 0 10px',
                  color: '#ffffff',
                  fontSize: '14px',
                }}
              >
                Sources
              </h4>

              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '7px',
                }}
              >
                {research.sources.map(
                  (source, index) => (
                    <a
                      key={`${source.url || index}`}
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: '#00d4ff',
                        fontSize: '12px',
                        textDecoration: 'none',
                        wordBreak: 'break-word',
                      }}
                    >
                      {index + 1}.{' '}
                      {source.title ||
                        source.url ||
                        'Source'}
                    </a>
                  )
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ======================================================
          SEARCH RESULTS
      ====================================================== */}

      {results.length > 0 && (
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
            marginBottom: '25px',
          }}
        >
          {results.map(renderResult)}
        </div>
      )}

      {/* ======================================================
          SELECTED WEBPAGE
      ====================================================== */}

      {selectedPage && (
        <div
          style={{
            marginTop: '25px',
            padding: '22px',
            borderRadius: '13px',
            border:
              '1px solid rgba(255,255,255,0.07)',
            background: 'rgba(255,255,255,0.025)',
          }}
        >
          {/* PAGE HEADER */}

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'flex-start',
              gap: '15px',
              marginBottom: '15px',
            }}
          >
            <div>
              <h3
                style={{
                  margin: 0,
                  color: '#ffffff',
                  fontSize: '18px',
                }}
              >
                📖 {selectedPage.title || 'Webpage'}
              </h3>

              <div
                style={{
                  marginTop: '5px',
                  color: '#666678',
                  fontSize: '11px',
                  wordBreak: 'break-all',
                }}
              >
                {selectedPage.final_url ||
                  selectedPage.url}
              </div>
            </div>

            <button
              type="button"
              onClick={() => setSelectedPage(null)}
              style={secondaryButtonStyle}
            >
              Close
            </button>
          </div>

          {/* PAGE STATS */}

          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
              marginBottom: '18px',
            }}
          >
            <span style={badgeStyle}>
              {selectedPage.character_count || 0}{' '}
              characters
            </span>

            {selectedPage.truncated && (
              <span style={badgeStyle}>
                Content truncated
              </span>
            )}
          </div>

          {/* PAGE TEXT */}

          <div
            style={{
              maxHeight: '420px',
              overflowY: 'auto',
              padding: '15px',
              borderRadius: '10px',
              background: '#09090e',
              color: '#bdbdc8',
              fontSize: '13px',
              lineHeight: '1.7',
              whiteSpace: 'pre-wrap',
              marginBottom: '18px',
            }}
          >
            {selectedPage.text ||
              'No readable text found.'}
          </div>

          {/* PAGE ACTIONS */}

          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
              marginBottom: '20px',
            }}
          >
            <button
              type="button"
              onClick={summarizePage}
              disabled={summaryLoading}
              style={primaryButtonStyle}
            >
              {summaryLoading
                ? 'Summarizing...'
                : '📝 Summarize'}
            </button>

            <a
              href={
                selectedPage.final_url ||
                selectedPage.url
              }
              target="_blank"
              rel="noopener noreferrer"
              style={{
                ...buttonStyle,
                textDecoration: 'none',
                display: 'inline-flex',
                alignItems: 'center',
              }}
            >
              🔗 Open Website
            </a>
          </div>

          {/* ==================================================
              SUMMARY
          ================================================== */}

          {summary && (
            <div
              style={{
                marginBottom: '20px',
                padding: '18px',
                borderRadius: '10px',
                background:
                  'rgba(0,212,255,0.035)',
                border:
                  '1px solid rgba(0,212,255,0.12)',
              }}
            >
              <h4
                style={{
                  margin: '0 0 10px',
                  color: '#ffffff',
                  fontSize: '15px',
                }}
              >
                📝 AI Summary
              </h4>

              <div
                style={{
                  color: '#c5c5cf',
                  fontSize: '13px',
                  lineHeight: '1.7',
                  whiteSpace: 'pre-wrap',
                }}
              >
                {summary}
              </div>
            </div>
          )}

          {/* ==================================================
              ASK PAGE
          ================================================== */}

          <div>
            <h4
              style={{
                margin: '0 0 10px',
                color: '#ffffff',
                fontSize: '15px',
              }}
            >
              ❓ Ask about this page
            </h4>

            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '8px',
              }}
            >
              <input
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === 'Enter') {
                    askAboutPage();
                  }
                }}
                placeholder="Ask something about this webpage..."
                style={{
                  flex: 1,
                  minWidth: '220px',
                  padding: '12px',
                  borderRadius: '9px',
                  border:
                    '1px solid rgba(255,255,255,0.08)',
                  background: '#0c0c12',
                  color: '#ffffff',
                  outline: 'none',
                  boxSizing: 'border-box',
                }}
              />

              <button
                type="button"
                onClick={askAboutPage}
                disabled={answerLoading}
                style={primaryButtonStyle}
              >
                {answerLoading
                  ? 'Thinking...'
                  : 'Ask PhantomAI'}
              </button>
            </div>
          </div>

          {/* PAGE ANSWER */}

          {pageAnswer && (
            <div
              style={{
                marginTop: '18px',
                padding: '18px',
                borderRadius: '10px',
                background:
                  'rgba(255,255,255,0.025)',
                border:
                  '1px solid rgba(255,255,255,0.07)',
              }}
            >
              <h4
                style={{
                  margin: '0 0 10px',
                  color: '#ffffff',
                  fontSize: '15px',
                }}
              >
                🤖 PhantomAI Answer
              </h4>

              <div
                style={{
                  color: '#c5c5cf',
                  fontSize: '13px',
                  lineHeight: '1.7',
                  whiteSpace: 'pre-wrap',
                }}
              >
                {pageAnswer}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ======================================================
          PAGE LOADING
      ====================================================== */}

      {pageLoading && (
        <div
          style={{
            padding: '25px',
            textAlign: 'center',
            color: '#77778a',
            fontSize: '13px',
          }}
        >
          📖 PhantomAI is reading the webpage...
        </div>
      )}

      {/* ======================================================
          NO RESULTS
      ====================================================== */}

      {!loading &&
        !researchLoading &&
        searchedQuery &&
        results.length === 0 &&
        !error &&
        !selectedPage && (
          <div
            style={{
              padding: '25px',
              textAlign: 'center',
              color: '#77778a',
              fontSize: '13px',
            }}
          >
            No search results found.
          </div>
        )}
    </div>
  );
};

// ============================================================
// STYLES
// ============================================================

const buttonStyle = {
  padding: '9px 13px',
  borderRadius: '8px',
  border: '1px solid rgba(255,255,255,0.08)',
  background: 'rgba(255,255,255,0.04)',
  color: '#d8d8df',
  fontSize: '12px',
  fontWeight: '600',
  cursor: 'pointer',
};

const primaryButtonStyle = {
  ...buttonStyle,
  border: 'none',
  background: 'rgba(0,212,255,0.9)',
  color: '#ffffff',
};

const researchButtonStyle = {
  ...buttonStyle,
  border:
    '1px solid rgba(150,100,255,0.3)',
  background:
    'rgba(150,100,255,0.12)',
  color: '#d8c8ff',
};

const secondaryButtonStyle = {
  ...buttonStyle,
  background: 'rgba(255,255,255,0.03)',
};

const badgeStyle = {
  padding: '5px 9px',
  borderRadius: '20px',
  background: 'rgba(255,255,255,0.05)',
  color: '#77778a',
  fontSize: '10px',
};

export default WebSearchTool;
