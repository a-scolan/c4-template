---
name: likec4-dsl
description: Use when working with `.c4`/`.likec4` files and exact LikeC4 DSL/CLI syntax is required (validate/export flags, predicates `*`/`_`/`**`, views, deployment, relationship extension matching, strict minimal snippets).
---

# LikeC4 DSL Skill

Architecture-as-code tool. Describe systems in `.c4`/`.likec4` files and LikeC4 generates interactive diagrams.

## Rules

1. **Projects** - it is possible to have multiple likec4 projects in a workspace, project is determined by presence of a config file (`.likec4rc`, `likec4.config.{ts,js,json}`). LikeC4 files belong to the project of the nearest config file in the directory hierarchy.
2. **Top-level statements** — only `import`, `specification`, `model`, `deployment`, `views`, `global` are allowed. Blocks can repeat, but at least one per file must be present.
3. **Multi-file merge** — Top-level blocks across files are merged. For example, `model { ... }` blocks present in multiple files, parsed separately, and then merged into a single model.
4. **Strings** — `'single'`, `"double"` — all support multi-line. Escape quotes with backslash: `\'` or `\"`.
5. **Markdown** — properties like `summary`/`description`/`notes` can contain Markdown. Use triple quotes `'''` or `"""`. Begin a new line after opening quotes and indent Markdown content for better formatting and syntax highlighting.
6. **Comments** — `// single line` and `/* multi-line */` comments supported anywhere.
7. **Identifier** — letters, digits, hyphens, underscores only. No dots (dots are FQN separators). Can't start with a digit. Examples: `customer`, `payment-service`, `frontendApp`, `quque-1`.
8. **FQN** — Fully Qualified Name (FQN) is a dot-separated path to an element, MUST be unique within the project. Examples: `customer`, `saas.backend.payment-service.paymentsApi`, `infra.eu.zone1.node1`.
9. **References** — LikeC4 has lexical scoping with hoisting, nested scope may shadow outer, like in JavaScript. To reference across files, FQN must be used.

## Response Discipline (critical for evals)

- If prompt says **"minimal"**, **"paste-ready"**, or **"strict"**, output exactly **one final command/snippet** (no alternatives, no fallback variants, no extra preamble).
- Do **not** add unrequested `title`, labels, alternate snippets, or long explanations unless explicitly asked.
- Prefer exact requested tokens/phrases in the first line when the prompt requires strict phrasing.
- For strict command prompts, avoid ambiguous wording like "equivalent command" unless prompt explicitly asks for alternatives.

## CLI Canonical Contracts (anti-substitution guardrails)

- Validate family: use `likec4 validate` (never substitute with `check`, `lint`, or `build`).
- Export family: use `likec4 export` (never substitute with other command families).
- Validation flags contract for strict evals: `--json --no-layout --file <path> ... <project-dir>`.
- Export output flags contract: prefer `--outdir` or `-o` (avoid invented aliases).

## Workflow

1. (Required) Find existing or create new project config (section below). Directory with project config defines the scope for all LikeC4 files in that directory and subdirectories. Ask user if you are uncertain about the scope.
2. (Required) Find existing or create new `specification { ... }`, this enables what kinds of elements/deployments/relationships/tags you can use. See Specification section below.
3. Architecture elements and relationships are defined in `model { ... }` block. See Model section below.
4. Deployment topology is defined in `deployment { ... }` block. See Deployment section below.
5. Views (diagrams) are defined in `views { ... }` block. See Views section below.
6. After editing LikeC4 files, validate with the CLI

## Generate → Self-check → Finalize

For strict command/snippet prompts, keep a compact loop:

1. **Generate** only the requested final command/snippet.
2. **Self-check** quickly: exact command family/flags, predicate semantics, scope/FQN correctness, relationship matcher specificity.
3. **Finalize** by fixing in place (no extra alternatives unless explicitly requested).

Never claim CLI execution happened unless it actually ran.

## Validation

```bash
<runtime> likec4 validate --json --no-layout --file <edited-file> <project-dir>
```

Runtime launchers are equivalent for this command family:

```bash
npx likec4 validate --json --no-layout --file <edited-file> <project-dir>
bunx likec4 validate --json --no-layout --file <edited-file> <project-dir>
pnpm dlx likec4 validate --json --no-layout --file <edited-file> <project-dir>
```

- `--json` — structured output (stdout), logging goes to stderr
- `--no-layout` — skip layout drift checks (faster, only syntax+semantic)
- `--file <path>` — only report errors from this file (can repeat for multiple files)
- `<project-dir>` — path to the project directory
- There is **no** `likec4 check` command; use `likec4 validate`.

For evals/gradings/executions, be **runner-tolerant** (`npx`/`bunx`/`pnpm dlx`), and judge correctness by subcommand + flags + project scope.

If workspace already has `likec4` as a dependency, check its version from package.json and ensure it is at least 1.53.0. If pinning is needed, use the active runner (`npx`/`bunx`/`pnpm dlx`) with `likec4@1.53.0`.

Example output:

```json
{
  "valid": false,
  "errors": [
    {
      "message": "...",
      "file": "/abs/path.c4",
      "line": 5,
      "range": { "start": { "line": 5, "character": 2 }, "end": { "line": 5, "character": 20 } }
    }
  ],
  "stats": {
    "totalFiles": 100, // Total number of files in the project
    "totalErrors": 500, // Total number of errors in the project
    "filteredFiles": 1, // Number of files that match the --file filter
    "filteredErrors": 1 // Number of errors in the filtered files
  }
}
```

Broken specification/model in a large project can cascade into lots of errors across all files. Always use `--file` to focus on the files you edited. If `filteredErrors` is 0 but `totalErrors` is high, your files are clean but something else in the project is broken (not your problem). Selfcheck that `filteredFiles` matches the number of files you passed to `--file`.

Field semantics (must be explicit in answers):

- `filteredFiles`: count of files actually included by repeated `--file` filters
- `filteredErrors`: errors in the filtered subset only
- `totalErrors`: errors across the full project model

Example edge case: if you pass 3 files but one is `likec4.config.json`, `filteredFiles` may be `2` because config JSON is not a `.c4`/`.likec4` source file for DSL validation.

## Export PNG flags (precision)

Canonical output directory flags:

- `--outdir` (long form)
- `-o` (short form)

Do not invent flags like `--out-dir`. Depending on LikeC4 version, `--output` may appear as compatibility alias; prefer `--outdir`/`-o` for deterministic answers.

Full CLI reference → `references/cli.md`

## LikeC4 Project Configuration

Config file (`likec4.config.json`, `.likec4rc`, or `likec4.config.{ts,js}`) defines a project. Its location sets the project scope (LikeC4 files belong to the project of the nearest config file in the directory hierarchy).

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "title": "Project Title"
}
```

Key options: `name` (required, unique ID in the workspace), `title` (display name)
Full reference → `references/configuration.md`

## Specification (Quick Reference)

Syntax:

```likec4
specification {
  // Define a tag, extra metadata, outside of specification used as #IDENTIFIER
  tag IDENTIFIER  
  // Define kind to use in model, with optional properties and style
  element IDENTIFIER {
    #tag-1 #tag-2 // tags to apply to all elements of this kind
    title "default title for this kind" // see Properties section below
    technology "default tech for this kind"
    description "default description for this kind"
    notation "legend title for this kind"
    style { ... } // see Style section below
  }
  // Define kind to use in deployment model
  deploymentNode IDENTIFIER {
    // same properties and styles as element kind
  }  
  // Define relationship kind with default properties and styles
  relationship IDENTIFIER {
    technology "default tech for this relationship kind"
    description "default description for this relationship kind"
    style { ... } // default style for this relationship kind
  }
  // Define custom color
  color IDENTIFIER #FFFFFF // or rgba(255,255,255,1)
}
```

**Important:**

- Specification is global, all defined kinds, tags etc. are available across all files in the project.
- Duplicate identifiers (same kind, same tag, etc.) will cause a validation error.
- Multiple specification blocks (in one file or across files) are allowed, but not recommended.
- Prefer to keep specification in a separate file, e.g. `specification.c4` (this improves responsiveness, as changes to the specification require parsing the entire model).

Example:

```likec4
specification {
  element actor { notation "Person" style { shape person } }
  element service { description "Same for all of the kind" style { shape component } }
  element webapp { style { shape browser } }
  element queue { style { shape queue color secondary } }

  relationship async { color amber; line dotted; head diamond; tail vee }

  tag deprecated
  tag critical

  deploymentNode environment { notation "Environment"; style { color gray } }
  deploymentNode vm
}
```

## Model (Quick Reference)

Model is a hierarchical structure of elements, where each element can contain other elements. Element MUST have a kind (from the specification) and an identifier (also known as name). Identifier MUST be unique within its parent. Element may have a body `{ .. }` with tags, properties, nested elements and relationships.
Relationships exist between any pair of elements, but not between parent-child elements. Relationships can be defined on any level of the hierarchy. Relationships, defined inside an element, implicitly have that element as their source.

Syntax:

```likec4
model {
  // Elements, top-levels are global, can be referenced anywhere in the project
  IDENTIFIER = KIND                   // without title, without body (title defaults to ID)
  IDENTIFIER = KIND "title"           // with title, without body
  KIND IDENTIFIER "title"             // if preferred by user to have kind before OD  
  IDENTIFIER = KIND {
    TAGS                              // optional, but must come first if present, before any properties
    PROPERTIES                        // optional, but must come before nested elements and relationships

    // order of nested elements vs relationships doesn't matter
    // Nested elements, can be referenced in this file by id, but from other files only using FQN, i.e. parentid.childid
    IDENTIFIER = KIND "Child Title" {
       // Same as above, no limit to nesting levels
    }
    KIND IDENTIFIER "Child Title" // if preferred by user to have kind before name

    // Explicit Relationship, SOURCE and TARGET must be resolvable within the current scope
    SOURCE -> TARGET
    // Implicit Relationship (current element is SOURCE)
    -> TARGET "Relationship title"
    -> TARGET "Relationship title" {
      TAGS                            // optional, but must come first if present, before any properties
      PROPERTIES                      // optional
    }
    // Relationship with kind
    -[REL_KIND]-> TARGET "Relationship title" 
    .REL_KIND -> TARGET "Relationship title"   // Alternative syntax for relationship with kind
    // "it" and "this" refer to the current element
    SOURCE -> it     // relationship to current element
    this -> TARGET   // relationship from current element
  }

  // Relationships on top level MUST have SOURCE
  SOURCE -> TARGET "Relationship title"    //without body
  SOURCE -> TARGET "Relationship title" {
    TAGS                                   // optional, but must come first if present, before any properties
    PROPERTIES                             // optional
  }
  SOURCE -[REL_KIND]-> TARGET
  SOURCE .REL_KIND TARGET

  // Extend existing element by FQN, e.g. from another file
  extend FQN { 
    TAGS                   // additional tags to apply to this element
    PROPERTIES             // additional properties to merge into this element, allowed `metadata` and `link` only

    NESTED_ELEMENTS | RELATIONSHIPS
  }
  // Extend existing relationship (must match existing relationship identity)
  // Anti-ambiguity matcher contract:
  // 1) SOURCE and TARGET are always required.
  // 2) If typed relationships exist, include KIND.
  // 3) If multiple relationships share SOURCE/TARGET/KIND, include TITLE.
  // In disambiguation cases, omitting KIND is WRONG (not just "ambiguous"): it can silently
  // match an unkinded relation instead of the intended typed one.
  extend SOURCE -> TARGET  {
    TAGS                   // additional tags to apply to this relationship
    PROPERTIES             // additional properties to merge into this relationship, allowed `metadata` and `link` only
  }
  extend SOURCE -[REL_KIND]-> TARGET "Relationship title" {
    TAGS                   // additional tags to apply to this relationship
    PROPERTIES             // additional properties to merge into this relationship, allowed `metadata` and `link` only
  }

  // Example:
  // Existing:
  //   frontend -> api "streams"
  //   frontend -[async]-> api "streams"
  // Wrong matcher for async target:
  //   extend frontend -> api "streams" { ... }
  // Correct matcher:
  //   extend frontend -[async]-> api "streams" { metadata { qos "high" } }
}
```

Example:

```likec4
model {
  customer = actor { 
    title "Customer" // Example `title` as property inside
    summary "Consumes Cloud Services"
    description """
      User with **active** subscription
      ... detailed description
    """
  }

  cloud = system "Cloud" {
    ui = container "Frontend" {
      technology "React"
      style { 
        shape browser
      }
      metadata { 
        version "1.0.0"
        owners ["Name 1", "Name 2"]
      }
      link https://github.com/likec4/likec4 "Repository"
      link ../relative/adr1.md
      link ../relative/adr2.md
      
      dashboard = app "Dashboard" {         
        icon tech:react
      }
    }
    backend = container "Backend" {
      api = service "API" { 
        #critical
        -[sql]-> db "reads/writes"
      }
      db = database "DB" {         
        style { 
          icon tech:postgresql
          shape storage
        }
      }
    }
    ui.dashboard -> backend.api { 
      title "calls"        // Example `title` as property inside  
      technology "HTTPS"
    }
  }

  customer -> cloud.ui.dashboard "browses" {
    metadata { 
      protocol "HTTPS"
    }
  }
}
```

**Element properties:** `title`, `description`, `summary`, `technology`, `metadata`, `style`, `icon`, `link`. If `description` exceeds 150 characters, add a `summary` with a shorter version (<150 chars) and keep the full details in `description`.

**Relationship properties:** `title`, `description`, `technology`, `metadata`, `style`, `link`, `navigateTo`

## Property (Quick Reference)

| Category        | Values                                                                                                                 |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **title**       | String, single line                                                                                                    |
| **description** | String, prefer to format with Markdown                                                                                 |
| **summary**     | String, short description, max 150 characters                                                                          |
| **technology**  | String, no multi-line                                                                                                  |
| **style**       | Syntax: `style { ... }`, see Style section below                                                                       |
| **icon**        | Shortcut for the `style { icon ... }`, takes precedence                                                                |
| **metadata**    | Syntax: `metadata { KEY VALUE }`, where key must follow identifiers format and value can be string or array of strings |
| **link**        | Syntax: `link URL "Optional title"`. May be used multiple times. URL can be relative to the document.                  |
| **navigateTo**  | ID of dynamic view to navigate to                                                                                      |

## Style (Quick Reference)

Style is a dict of properties to define the visual appearance, example:

```likec4
style {
  color primary   
  icon tech:claude
}
```

| style property   | Values                                                                                                                                 |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **color**        | `primary`, `secondary`, `muted`, `slate`, `blue`, `indigo`, `sky`, `red`, `gray`, `green`, `amber`, or custom color from specification |
| **shape**        | `rectangle`, `component`, `person`, `browser`, `mobile`, `cylinder`, `storage`, `queue`, `bucket`, `document`                          |
| **border**       | `solid`, `dashed`, `dotted`, `none`                                                                                                    |
| **opacity**      | `0%` - `100%`                                                                                                                          |
| **size**         | `xs`, `sm`, `md`, `lg`, `xl`                                                                                                           |
| **padding**      | same as size                                                                                                                           |
| **textSize**     | same as size                                                                                                                           |
| **icon**         | relative path, URL, or from icon pack (`aws:`, `azure:`, `gcp:`, `tech:`, `bootstrap:`)                                                |
| **iconColor**    | same as color                                                                                                                          |
| **iconSize**     | same as size                                                                                                                           |
| **iconPosition** | `top`, `left`, `right`, `bottom`                                                                                                       |
| **multiple**     | `true`/`false`                                                                                                                         |

Icon pack is a bundled set of icons, referenced by prefix.
For example, `icon aws:simple-storage-service` will use `@likec4/icons/aws/simple-storage-service` (scan package to find available icons, use lower-kebab-case).

Relationship style properties:

- `color` (line color): same as element colors
- `line` (line style): `solid`, `dashed`, `dotted`
- `head` (arrow style on head, i.e to TARGET): `none`, `normal`, `onormal`, `dot`, `odot`, `diamond`, `odiamond`, `crow`, `open`, `vee`
- `tail` (arrow style on tail, i.e to SOURCE): same as for `head`

## Deployment (Quick Reference)

Deployment has same syntax as model, but is defined in `deployment` block and uses `deploymentNode` kinds.
The deployment model maps logical architecture elements to physical infrastructure, allowing to "deploy" instances of elements from the model inside deployment nodes using the `instanceOf` keyword.

```likec4
deployment {
  IDENTIFIER = DEPLOYMENT_KIND {
    TAGS
    PROPERTIES

    instanceOf ELEMENT_ID
    IDENTIFIER = instanceOf ELEMENT_ID {
      TAGS
      PROPERTIES
    }
  }
}
```

Example:

```likec4
specification {
  element webapp
  deploymentNode vm
}
model {
  webapp myapp
}
deployment {
  vm vm1 {
    instanceOf myapp
  }
  vm vm2 {
    // Named instances of same element within the same deployment node
    instance1 = instanceOf myapp
    instance2 = instanceOf myapp
  }
}
```

Deployment model inherits relationships from the logical model, but allows to define additional relationships between deployment nodes/instances (using same syntax as in model).

## Views (Quick Reference)

Element/deployment views show elements/relationships from the model/deployment.
Dynamic views show interactions between elements. They can render as animated flow diagrams or UML sequence diagrams.

Syntax:

```likec4
views {
  // element view
  view IDENTIFIER {
    TAGS                // optional tags, must come first if present, before any properties
    PROPERTIES          // optional, but must come before any view rules
    ELEMENT_VIEW_RULES    
  }
  // element view can also be scoped to a specific element, explained below
  view IDENTIFIER of ELEMENT_ID {     
    TAGS
    PROPERTIES
    ELEMENT_VIEW_RULES    
  }
  // dynamic views
  dynamic view IDENTIFIER {
    TAGS
    PROPERTIES  
    DYNAMIC_VIEW_RULES
  }
  // deployment views
  deployment view IDENTIFIER {
    TAGS
    PROPERTIES
    DEPLOYMENT_VIEW_RULES
  }
}
```

**View properties:** `title`, `description`, `metadata`, `link`

Full view reference → references/views.md

## Quick Decision Trees

### "I need incoming relationship predicates"

```text
Need inbound relation selection?
├─ From any source to target element → `include -> target`
├─ From explicit wildcard source     → `include * -> target`
└─ Include both directions around X  → `include -> X ->`
```

`include -> X` and `include * -> X` are related but not interchangeable in all contexts; prefer the exact form requested by user/eval.

### Scoped Predicate Truth Card (`*`, `_`, `**`)

| Selector | One-line truth | Typical use |
| --- | --- | --- |
| `parent.*` | Direct children of `parent` only | Show immediate structure |
| `parent._` | Direct children of `parent` that have relationships with accumulated result | Keep only connected direct children |
| `parent.**` | Recursive descendants of `parent` that have relationships with accumulated result | Explore connected deep descendants |

Hard rule: do not describe `*` as recursive; do not describe `_` as wildcard-all; do not drop relationship-condition semantics for `_` / `**`.

### "I need to create a diagram/view or show a flow or sequence"

```text
What kind of diagram?
├─ Interaction flow / sequence → Dynamic View
├─ Infrastructure / deployment → Deployment View
├─ From architecture model → Element View
│   ├─ Primary element known → Scoped view: `view name of element { ... }`
│   └─ Extend existing view → `view name extends other { ... }`
└─ Other → `view name { ... }`
```

### "I need to style ..."

```text
Styling?
├─ Style element(s) in a view → view `style` rule, see `references/views.md`
├─ Style element(s) in some views, but not all
│   ├─ views in same file → local view rule, see `references/views.md`
│   └─ views in different files → global view rule, see `references/views.md`
├─ Style element globally → property inside element definition, see Model section
├─ Style all elements of a kind → property inside kind specification, see Specification section
├─ Style by tag → view rule, see `references/views.md`
├─ Style relationship(s) in a view → view rule, see `references/views.md`
├─ Style relationship globally → property inside relationship definition, see Model section
├─ Style all relationships of a kind → property inside kind specification, see Specification section
├─ Reuse same styles across views → see `references/views.md`
```

### "I need to organize across files"

```text
Multi-file project?
├─ Import elements → import { backend } from './shared.c4'
├─ Extend element → extend cloud.backend { service newSvc "New" }
├─ Extend relationship → extend cloud -> amazon { metadata { ... } }
├─ Metadata merge → Duplicate keys become arrays
├─ Organize views → views "Use Cases" { ... } (folder label)
└─ All blocks are mergeable across files
```

### "I need to show a flow or sequence"

```text
Flow / sequence diagram?
├─ Basic steps → source -> target "title"
├─ Response / backward → source <- target "returns"
├─ Parallel actions → parallel { ... } (also: par { ... })
├─ Chained steps → customer -> frontend "x" -> backend "y"
├─ Step with notes → step { notes 'Markdown content' }
├─ Link to another view → step { navigateTo other-view }
├─ Sequence variant → dynamic view name { variant sequence }
└─ Full reference → references/dynamic-views.md

## Anti-Patterns to Avoid in Strict Prompts

| Anti-pattern | Why it fails | Correct behavior |
| --- | --- | --- |
| Substituting command families (`check`/`build`) for `validate` | Breaks exact command contract | Keep `likec4 validate` |
| Inventing/guessing flags | Creates non-portable invalid commands | Use canonical documented flags only |
| Multiple alternative snippets for one strict ask | Reduces precision; fails strict-output grading | Output one final answer unless alternatives are requested |
| Extending typed relationship without kind/title in ambiguous graph | Can target wrong relationship | Match with source + target + kind (+ title when needed) |
```

## Reference Index

| File                          | Purpose                                                                          |
| ----------------------------- | -------------------------------------------------------------------------------- |
| `references/cli.md`           | CLI commands: serve, build, export, codegen, mcp, format                         |
| `references/configuration.md` | Project config options, multi-project setup, styles, generators, include/exclude |
| `references/views.md`         | View rules, include/exclude, style rules, groups, autoLayout                     |
| `references/predicates.md`    | Predicate syntax, wildcards, where conditions, with overrides, global groups     |
| `references/examples.md`      | Compact real-world examples: extend, groups, globals, dynamic, deployment, rank  |
