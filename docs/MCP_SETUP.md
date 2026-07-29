# MCP Servers Configuration Guide
## Import Management System — Model Context Protocol Setup

> **Config File:** `C:\Users\Kamal Pc\.gemini\config\mcp_config.json`  
> **Restart Required:** Yes — restart Antigravity IDE after any config change.

---

## Configured MCP Servers (8 + 1 existing)

| # | Server | Package / Command | Status |
|---|--------|-------------------|--------|
| 1 | **filesystem** | `@modelcontextprotocol/server-filesystem` (npx) | ✅ Configured |
| 2 | **git** | `mcp-server-git` (uvx) | ✅ Configured |
| 3 | **sqlite** | `mcp-server-sqlite` (uvx) | ✅ Configured |
| 4 | **context7** | `@upstash/context7-mcp` (npx) | ✅ Configured |
| 5 | **sequential-thinking** | `@modelcontextprotocol/server-sequential-thinking` (npx) | ✅ Configured |
| 6 | **memory** | `@modelcontextprotocol/server-memory` (npx) | ✅ Configured |
| 7 | **mermaid** | `@peng-shawn/mermaid-mcp-server` (npx) | ✅ Configured |
| 8 | **pdf** | `@anaisbetts/mcp-pdf` (npx) | ✅ Configured |
| 9 | **laravel-boost** | PHP Artisan (existing) | ✅ Kept |

---

## What Each Server Does

### 1. 📁 Filesystem MCP
**Purpose:** Read, write, create, and manage files and directories directly.  
**Allowed Paths:**
- `i:\disktop` — Main project directory
- `C:\Users\Kamal Pc\Desktop`
- `C:\Users\Kamal Pc\Documents`

**Use for:**
- Reading source code files
- Creating/editing project files
- Listing directory contents
- Moving and copying files

---

### 2. 🔀 Git MCP
**Purpose:** Full Git operations on the project repository.  
**Repository:** `i:\disktop`

**Use for:**
- `git status`, `git diff`, `git log`
- Creating commits
- Reading branch history
- Viewing file changes between commits

---

### 3. 🗄️ SQLite MCP
**Purpose:** Query and manage the SQLite database directly.  
**Database:** `i:\disktop\import_system.db`

**Use for:**
- Running SQL SELECT queries
- Inspecting table schemas
- Debugging data issues
- Verifying business rule data

---

### 4. 📚 Context7 MCP
**Purpose:** Fetch live, up-to-date documentation for any library or framework.

**Use for:**
- Getting accurate PySide6 / Qt6 API documentation
- Checking SQLAlchemy, Pydantic, Alembic docs
- Verifying exact method signatures before coding
- Avoiding hallucinated API calls

**Example queries:**
```
context7: "PySide6 QTableWidget setRowHeight"
context7: "SQLAlchemy 2.0 Session.execute"
```

---

### 5. 🧠 Sequential Thinking MCP
**Purpose:** Structured, step-by-step reasoning for complex problems.

**Use for:**
- Planning large features before implementation
- Debugging complex multi-step issues
- Architectural decisions
- Breaking down ambiguous requirements

---

### 6. 💾 Memory MCP
**Purpose:** Persistent memory across conversations using a knowledge graph.

**Use for:**
- Remembering project-specific decisions
- Storing design system rules
- Tracking which features are implemented
- Maintaining context across long sessions

---

### 7. 📊 Mermaid MCP
**Purpose:** Generate and render Mermaid diagrams as images.

**Use for:**
- Generating ER diagrams from the schema
- Creating workflow / flowchart diagrams
- Architecture diagrams
- UI navigation flow diagrams

---

### 8. 📄 PDF MCP
**Purpose:** Read and extract text content from PDF files.

**Use for:**
- Reading supplier documents or import contracts
- Extracting data from customs PDF reports
- Reading uploaded specification PDFs

---

## Configuration File Location

```
C:\Users\Kamal Pc\.gemini\config\mcp_config.json
```

## Adding More Allowed Filesystem Paths

Edit the `filesystem` entry in `mcp_config.json` and add more paths to the `args` array:

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "i:\\disktop",
    "C:\\Users\\Kamal Pc\\Desktop",
    "C:\\new\\path\\here"
  ]
}
```

## Changing the SQLite Database Path

Edit the `sqlite` entry:

```json
"sqlite": {
  "command": "uvx",
  "args": [
    "mcp-server-sqlite",
    "--db-path",
    "i:\\disktop\\import_system.db"
  ]
}
```

---

> **Note:** After modifying `mcp_config.json`, restart Antigravity IDE for changes to take effect.
