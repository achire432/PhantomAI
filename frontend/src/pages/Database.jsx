import React, { useEffect, useState } from 'react';
import { tools } from '../api/endpoints';

const Database = () => {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState(null);
  const [tableData, setTableData] = useState(null);

  const [query, setQuery] = useState(
    'SELECT id, full_name, email, role FROM users LIMIT 100'
  );

  const [queryResult, setQueryResult] = useState(null);

  const [loadingTables, setLoadingTables] = useState(true);
  const [loadingTable, setLoadingTable] = useState(false);
  const [runningQuery, setRunningQuery] = useState(false);

  const [error, setError] = useState('');

  useEffect(() => {
    loadTables();
  }, []);

  const loadTables = async () => {
    setLoadingTables(true);
    setError('');

    try {
      const response = await tools.database.tables();

      const data = response.data;

      if (Array.isArray(data)) {
        setTables(data);
      } else if (Array.isArray(data?.tables)) {
        setTables(data.tables);
      } else if (Array.isArray(data?.data)) {
        setTables(data.data);
      } else {
        setTables([]);
      }
    } catch (err) {
      console.error('Failed to load database tables:', err);

      setError(
        err.response?.data?.detail ||
        'Unable to load database tables.'
      );
    } finally {
      setLoadingTables(false);
    }
  };

  const selectTable = async (tableName) => {
    setSelectedTable(tableName);
    setLoadingTable(true);
    setError('');
    setQueryResult(null);

    try {
      const response = await tools.database.table(tableName);

      setTableData(response.data);
    } catch (err) {
      console.error('Failed to load table:', err);

      setError(
        err.response?.data?.detail ||
        'Unable to load table.'
      );

      setTableData(null);
    } finally {
      setLoadingTable(false);
    }
  };

  const runQuery = async () => {
    if (!query.trim() || runningQuery) return;

    setRunningQuery(true);
    setError('');
    setQueryResult(null);

    try {
      const response = await tools.database.query(query);

      setQueryResult(response.data);
    } catch (err) {
      console.error('Database query failed:', err);

      setError(
        err.response?.data?.detail ||
        'Database query failed.'
      );
    } finally {
      setRunningQuery(false);
    }
  };

  const getRows = (data) => {
    if (!data) return [];

    if (Array.isArray(data)) return data;

    if (Array.isArray(data.data)) return data.data;

    if (Array.isArray(data.rows)) return data.rows;

    return [];
  };

  const getColumns = (data, rows) => {
    if (data?.columns && Array.isArray(data.columns)) {
      return data.columns;
    }

    if (rows.length > 0) {
      return Object.keys(rows[0]);
    }

    return [];
  };

  const renderTable = (data) => {
    const rows = getRows(data);
    const columns = getColumns(data, rows);

    if (!rows.length) {
      return (
        <div style={styles.empty}>
          No rows returned.
        </div>
      );
    }

    return (
      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column} style={styles.th}>
                  {column}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {rows.map((row, index) => (
              <tr key={index}>
                {columns.map((column) => (
                  <td key={column} style={styles.td}>
                    {row[column] === null ||
                    row[column] === undefined ? (
                      <span style={styles.nullValue}>
                        NULL
                      </span>
                    ) : (
                      String(row[column])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div style={styles.page}>
      {/* HEADER */}

      <div style={styles.header}>
        <div>
          <div style={styles.titleRow}>
            <span style={styles.databaseIcon}>🗄️</span>

            <h1 style={styles.title}>
              Database
            </h1>

            <span style={styles.liveBadge}>
              ● CONNECTED
            </span>
          </div>

          <p style={styles.subtitle}>
            Explore and inspect your PhantomAI database.
          </p>
        </div>

        <button
          onClick={loadTables}
          style={styles.refreshButton}
        >
          ↻ Refresh
        </button>
      </div>

      {error && (
        <div style={styles.error}>
          <span>⚠</span>
          <span>{error}</span>
        </div>
      )}

      {/* MAIN LAYOUT */}

      <div style={styles.layout}>
        {/* TABLE LIST */}

        <aside style={styles.tableSidebar}>
          <div style={styles.sidebarHeader}>
            <span>DATABASE TABLES</span>

            <span style={styles.tableCount}>
              {tables.length}
            </span>
          </div>

          {loadingTables ? (
            <div style={styles.loading}>
              Loading tables...
            </div>
          ) : tables.length === 0 ? (
            <div style={styles.emptySidebar}>
              No tables found.
            </div>
          ) : (
            <div style={styles.tableList}>
              {tables.map((table, index) => {
                const tableName =
                  typeof table === 'string'
                    ? table
                    : table.table_name ||
                      table.name ||
                      table.table ||
                      Object.values(table)[0];

                const active =
                  selectedTable === tableName;

                return (
                  <button
                    key={`${tableName}-${index}`}
                    onClick={() =>
                      selectTable(tableName)
                    }
                    style={{
                      ...styles.tableItem,
                      ...(active
                        ? styles.tableItemActive
                        : {}),
                    }}
                  >
                    <span style={styles.tableIcon}>
                      ▦
                    </span>

                    <span>{tableName}</span>
                  </button>
                );
              })}
            </div>
          )}
        </aside>

        {/* CONTENT */}

        <section style={styles.content}>
          {/* TABLE VIEW */}

          <div style={styles.panel}>
            <div style={styles.panelHeader}>
              <div>
                <div style={styles.panelTitle}>
                  {selectedTable
                    ? `Table: ${selectedTable}`
                    : 'Select a table'}
                </div>

                {selectedTable &&
                  tableData && (
                    <div style={styles.panelMeta}>
                      {getRows(tableData).length}{' '}
                      rows
                    </div>
                  )}
              </div>

              {loadingTable && (
                <span style={styles.loadingText}>
                  Loading...
                </span>
              )}
            </div>

            {selectedTable && tableData ? (
              renderTable(tableData)
            ) : (
              <div style={styles.placeholder}>
                <div style={styles.placeholderIcon}>
                  🗄️
                </div>

                <div>
                  Select a table from the left
                </div>

                <small>
                  PhantomAI will load its records here.
                </small>
              </div>
            )}
          </div>

          {/* SQL QUERY */}

          <div style={styles.queryPanel}>
            <div style={styles.queryHeader}>
              <div>
                <div style={styles.panelTitle}>
                  SQL Query
                </div>

                <div style={styles.panelMeta}>
                  Read-only database explorer
                </div>
              </div>

              <span style={styles.selectOnly}>
                SELECT ONLY
              </span>
            </div>

            <textarea
              value={query}
              onChange={(e) =>
                setQuery(e.target.value)
              }
              spellCheck={false}
              style={styles.editor}
              placeholder="SELECT * FROM users LIMIT 100"
            />

            <div style={styles.queryFooter}>
              <div style={styles.queryHint}>
                Multiple SQL statements are not allowed.
              </div>

              <button
                onClick={runQuery}
                disabled={
                  runningQuery ||
                  !query.trim()
                }
                style={{
                  ...styles.runButton,
                  opacity:
                    runningQuery ||
                    !query.trim()
                      ? 0.5
                      : 1,
                }}
              >
                {runningQuery
                  ? 'Running...'
                  : '▶ Run Query'}
              </button>
            </div>
          </div>

          {/* QUERY RESULTS */}

          {queryResult && (
            <div style={styles.panel}>
              <div style={styles.panelHeader}>
                <div>
                  <div style={styles.panelTitle}>
                    Query Results
                  </div>

                  <div style={styles.panelMeta}>
                    {queryResult.row_count ??
                      getRows(queryResult).length}{' '}
                    rows returned
                  </div>
                </div>

                <span style={styles.successBadge}>
                  ✓ SUCCESS
                </span>
              </div>

              {renderTable(queryResult)}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: '100vh',
    padding: '32px',
    color: '#fff',
    background:
      'linear-gradient(180deg, rgba(5,5,12,0.92), rgba(5,5,9,0.96))',
  },

  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '28px',
  },

  titleRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },

  databaseIcon: {
    fontSize: '28px',
  },

  title: {
    margin: 0,
    fontSize: '28px',
    fontWeight: 700,
  },

  subtitle: {
    margin: '8px 0 0 42px',
    color: '#77778b',
    fontSize: '13px',
  },

  liveBadge: {
    padding: '5px 9px',
    borderRadius: '20px',
    background: 'rgba(70,220,130,0.1)',
    border: '1px solid rgba(70,220,130,0.25)',
    color: '#5fe38b',
    fontSize: '10px',
    fontWeight: 700,
    letterSpacing: '0.5px',
  },

  refreshButton: {
    padding: '10px 15px',
    background: 'rgba(0,212,255,0.08)',
    border: '1px solid rgba(0,212,255,0.25)',
    borderRadius: '9px',
    color: '#00d4ff',
    cursor: 'pointer',
    fontSize: '13px',
  },

  error: {
    display: 'flex',
    gap: '10px',
    padding: '12px 15px',
    marginBottom: '18px',
    background: 'rgba(220,70,70,0.08)',
    border: '1px solid rgba(220,70,70,0.25)',
    borderRadius: '9px',
    color: '#ff7777',
    fontSize: '13px',
  },

  layout: {
    display: 'grid',
    gridTemplateColumns: '230px minmax(0, 1fr)',
    gap: '18px',
    alignItems: 'start',
  },

  tableSidebar: {
    background: 'rgba(12,12,20,0.78)',
    border: '1px solid rgba(255,255,255,0.06)',
    borderRadius: '13px',
    overflow: 'hidden',
    minHeight: '500px',
  },

  sidebarHeader: {
    padding: '15px',
    borderBottom:
      '1px solid rgba(255,255,255,0.06)',
    color: '#77778b',
    fontSize: '10px',
    fontWeight: 700,
    letterSpacing: '1px',
    display: 'flex',
    justifyContent: 'space-between',
  },

  tableCount: {
    color: '#00d4ff',
  },

  tableList: {
    padding: '8px',
  },

  tableItem: {
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '11px 10px',
    marginBottom: '3px',
    background: 'transparent',
    border: '1px solid transparent',
    borderRadius: '8px',
    color: '#aaaabd',
    cursor: 'pointer',
    textAlign: 'left',
    fontSize: '13px',
  },

  tableItemActive: {
    background: 'rgba(0,212,255,0.09)',
    border:
      '1px solid rgba(0,212,255,0.2)',
    color: '#00d4ff',
  },

  tableIcon: {
    fontSize: '17px',
  },

  loading: {
    padding: '20px',
    color: '#00d4ff',
    fontSize: '12px',
  },

  emptySidebar: {
    padding: '20px',
    color: '#666679',
    fontSize: '12px',
  },

  content: {
    minWidth: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: '18px',
  },

  panel: {
    background: 'rgba(12,12,20,0.78)',
    border:
      '1px solid rgba(255,255,255,0.06)',
    borderRadius: '13px',
    overflow: 'hidden',
  },

  panelHeader: {
    padding: '15px 18px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom:
      '1px solid rgba(255,255,255,0.06)',
  },

  panelTitle: {
    color: '#fff',
    fontSize: '14px',
    fontWeight: 600,
  },

  panelMeta: {
    color: '#626276',
    fontSize: '11px',
    marginTop: '4px',
  },

  loadingText: {
    color: '#00d4ff',
    fontSize: '11px',
  },

  tableWrapper: {
    width: '100%',
    overflowX: 'auto',
  },

  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '12px',
  },

  th: {
    padding: '11px 14px',
    textAlign: 'left',
    color: '#00d4ff',
    background: 'rgba(0,212,255,0.035)',
    borderBottom:
      '1px solid rgba(255,255,255,0.06)',
    fontWeight: 600,
    whiteSpace: 'nowrap',
  },

  td: {
    padding: '11px 14px',
    color: '#c7c7d3',
    borderBottom:
      '1px solid rgba(255,255,255,0.04)',
    whiteSpace: 'nowrap',
  },

  nullValue: {
    color: '#555567',
    fontStyle: 'italic',
  },

  placeholder: {
    minHeight: '260px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    color: '#656579',
    fontSize: '13px',
  },

  placeholderIcon: {
    fontSize: '42px',
    opacity: 0.5,
  },

  queryPanel: {
    background: 'rgba(8,8,15,0.9)',
    border:
      '1px solid rgba(0,212,255,0.12)',
    borderRadius: '13px',
    overflow: 'hidden',
  },

  queryHeader: {
    padding: '15px 18px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom:
      '1px solid rgba(255,255,255,0.06)',
  },

  selectOnly: {
    padding: '5px 8px',
    borderRadius: '5px',
    color: '#ffca6a',
    background: 'rgba(255,202,106,0.08)',
    border:
      '1px solid rgba(255,202,106,0.18)',
    fontSize: '9px',
    fontWeight: 700,
  },

  editor: {
    width: '100%',
    minHeight: '130px',
    resize: 'vertical',
    boxSizing: 'border-box',
    padding: '18px',
    background: '#08080f',
    border: 'none',
    outline: 'none',
    color: '#cfefff',
    fontSize: '13px',
    lineHeight: 1.6,
    fontFamily:
      'SFMono-Regular, Menlo, Monaco, Consolas, monospace',
  },

  queryFooter: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '10px 14px',
    borderTop:
      '1px solid rgba(255,255,255,0.05)',
  },

  queryHint: {
    color: '#555568',
    fontSize: '10px',
  },

  runButton: {
    padding: '9px 15px',
    border: 'none',
    borderRadius: '7px',
    background: '#00d4ff',
    color: '#050509',
    fontWeight: 700,
    fontSize: '11px',
    cursor: 'pointer',
  },

  successBadge: {
    color: '#5fe38b',
    fontSize: '10px',
    fontWeight: 700,
  },

  empty: {
    padding: '30px',
    textAlign: 'center',
    color: '#626276',
    fontSize: '12px',
  },
};

export default Database;