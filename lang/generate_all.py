# Generator for language tutorials (same tab structure as python)
import pathlib

BASE = pathlib.Path(r'C:/Users/erich/.cline/data/workspaces/chat/coding-hub/lang')

def build(lang, d):
    parts = []
    parts.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Learn {d['name']} from zero. Free tutorial with Beginner, Intermediate, and Advanced levels." />
  <meta name="theme-color" content="#4f46e5" />
  <title>{d['name']} Tutorial — CodeHub</title>
  <link rel="stylesheet" href="../css/styles.css" />
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><div class="container nav"><a class="brand" href="../index.html" aria-label="CodeHub home"><span class="logo" aria-hidden="true"></></span><span>CodeHub</span></a><button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button><nav aria-label="Primary"><ul class="nav-links"><li><a href="../index.html">Home</a></li><li><a href="../languages.html" class="active">Languages</a></li><li><a href="../index.html#start">Start Here</a></li><li><a href="../index.html#faq">FAQ</a></li></ul></nav><button class="theme-toggle" aria-label="Switch to dark mode">🌙</button></div></header>
  <main id="main">
    <nav class="breadcrumb container" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>›</span><a href="../languages.html">Languages</a><span>›</span><span aria-current="page">{d['name']}</span></nav>
    <div class="container tutorial-layout">
      <aside class="toc" aria-label="Table of contents"><h4>Contents</h4><ul><li><a href="#what">What is {d['name']}?</a></li><li><a href="#setup">Run Online (No Install)</a></li><li><a href="#beginner">Beginner</a></li><li><a href="#intermediate">Intermediate</a></li><li><a href="#advanced">Advanced</a></li><li><a href="#next">What's Next?</a></li></ul></aside>
      <article class="lesson">
        <h1>{d['emoji']} {d['name']} — Learn From Zero</h1>
        <p class="callout play"><span class="ico" aria-hidden="true">🎮</span><strong>Playground:</strong> {d['playground']} — click, type, run.</p>

        <section id="what"><h2>What is {d['name']}?</h2>{d['what']}</section>

        <section id="setup"><h2>Run Online — No Install</h2><p>Use the playground links above.</p></section>

        <!-- LEVEL TABS -->
        <div class="level-tabs" role="tablist" aria-label="Difficulty level">
          <button class="level-tab" role="tab" aria-selected="true" data-level="beginner" id="tab-beginner">🟢 Beginner</button>
          <button class="level-tab" role="tab" aria-selected="false" data-level="intermediate" id="tab-intermediate">🟡 Intermediate</button>
          <button class="level-tab" role="tab" aria-selected="false" data-level="advanced" id="tab-advanced">🔴 Advanced</button>
        </div>

        <!-- BEGINNER PANEL -->
        <section id="beginner" class="level-panel" data-level="beginner" role="tabpanel" aria-labelledby="tab-beginner">
          <h2>🟢 Beginner — Core Basics</h2>
''')
    for sid, title, code, note in d["beginner"]:
        parts.append(f'''          <section id="{sid}"><h3>{title}</h3><div class="codeblock"><div class="cb-head"><span class="cb-lang">{lang}</span><button class="copy-btn" aria-label="Copy code">Copy</button></div><pre><code>{code}</code></pre></div><p>{note}</p></section>
''')
    parts.append('''        </section>

        <!-- INTERMEDIATE PANEL -->
        <section id="intermediate" class="level-panel" data-level="intermediate" role="tabpanel" aria-labelledby="tab-intermediate">
          <h2>🟡 Intermediate — Building Real Programs</h2>
''')
    for sid, title, code, note in d["intermediate"]:
        parts.append(f'''          <section id="{sid}"><h3>{title}</h3><div class="codeblock"><div class="cb-head"><span class="cb-lang">{lang}</span><button class="copy-btn" aria-label="Copy code">Copy</button></div><pre><code>{code}</code></pre></div><p>{note}</p></section>
''')
    parts.append('''        </section>

        <!-- ADVANCED PANEL -->
        <section id="advanced" class="level-panel" data-level="advanced" role="tabpanel" aria-labelledby="tab-advanced">
          <h2>🔴 Advanced — Pro Concepts</h2>
''')
    for sid, title, code, note in d["advanced"]:
        parts.append(f'''          <section id="{sid}"><h3>{title}</h3><div class="codeblock"><div class="cb-head"><span class="cb-lang">{lang}</span><button class="copy-btn" aria-label="Copy code">Copy</button></div><pre><code>{code}</code></pre></div><p>{note}</p></section>
''')
    parts.append('''        </section>

        <section id="next"><h2>What's Next?</h2><ul><li>Build a tiny project: <em>Calculator</em>, <em>To-Do App</em>, <em>Weather Widget</em></li><li>Read the official docs and a good book</li><li>Solve <a href="https://exercism.org" target="_blank" rel="noopener">Exercism</a> exercises</li><li>Join a community &amp; share your code</li></ul><p class="callout play"><span class="ico" aria-hidden="true">🎮</span>Practice daily for 20 minutes. Consistency &gt; intensity.</p></section>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container"><div class="footer-bottom"><p>© <span id="year"></span> CodeHub. Free for everyone.</p></div></div></footer>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
  <script src="../js/main.js"></script>
</body>
</html>''')
    return "".join(parts)

# ---- Language data ----
LANGS = {}

LANGS["javascript"] = dict(
    emoji="\U0001f4a5", name="JavaScript",
    playground='<a href="https://replit.com/languages/javascript" target="_blank" rel="noopener">Replit JS</a> | <a href="https://jsfiddle.net" target="_blank" rel="noopener">JSFiddle</a>',
    what="<p>JavaScript is the <strong>language of the web</strong>. It runs in every browser and now also on servers (Node.js). It's event-driven and great for interactive apps.</p><ul><li>Websites &amp; SPAs (React, Vue, Svelte)</li><li>Backend (Node.js, Express, NestJS)</li><li>Mobile (React Native) &amp; Desktop (Electron)</li><li>Games &amp; automation</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'console.log("Hello, world!");', 'Use <code>console.log()</code> to print to the console.'),
        ("vars", "Variables & Types", 'let name = "Ada";\nconst age = 36;\nlet isStudent = true;\nconsole.log(name, age, isStudent);', "Use <code>let</code> (reassignable) and <code>const</code> (constant). Avoid <code>var</code>."),
        ("control", "If / Else", 'const age = 18;\nif (age >= 18) console.log("Vote");\nelse console.log("Too young");', "Curly braces <code>{}</code> group statements."),
        ("loops", "Loops", 'for (let i = 0; i < 5; i++) console.log(i);\nlet n = 3;\nwhile (n-- > 0) console.log(n);', "Use <code>for...of</code> for arrays, <code>for...in</code> for object keys."),
        ("functions", "Functions", 'function greet(name) {\n  return `Hello, ${name}!`;\n}\nconsole.log(greet("World"));', "Arrow functions: <code>const add = (a,b) =&gt; a + b;</code>"),
        ("arrays", "Arrays & Objects", 'const fruits = ["apple", "banana"];\nfruits.push("cherry");\nconst person = { name: "Ada", age: 36 };\nconsole.log(fruits[0], person.name);', "Arrays are dynamic; objects use <code>key: value</code>."),
    ],
    intermediate=[
        ("modules", "Modules (ESM)", '// math.js\nfunction add(a, b) { return a + b; }\nexport { add };\n// main.js\nimport { add } from "./math.js";\nconsole.log(add(2, 3));', "Modern JS uses <code>import</code>/<code>export</code>."),
        ("dom", "DOM & Events", 'document.querySelector("#btn").addEventListener("click", () => {\n  alert("Clicked!");\n});', "<code>querySelector</code> finds elements in the DOM."),
        ("async", "Promises & async/await", 'async function load() {\n  const res = await fetch("/api/data");\n  const data = await res.json();\n  console.log(data);\n}', "Wrap <code>await</code> in <code>try/catch</code>."),
        ("classes", "Classes", 'class Animal {\n  constructor(name) { this.name = name; }\n  speak() { return this.name + " sounds"; }\n}\nconst dog = new Animal("Rex");', "Classes are sugar over prototypal inheritance."),
        ("spread", "Spread & Destructuring", 'const more = [...[1,2,3], 4];\nconst [first, ...rest] = more;\nconst { name } = { name: "Ada", age: 36 };', "Spread <code>...</code> copies/merges."),
    ],
    advanced=[
        ("closures", "Closures", 'function makeCounter() {\n  let count = 0;\n  return () => ++count;\n}\nconst c = makeCounter();\nc(); c();', "A closure remembers its lexical scope."),
        ("proxies", "Proxies", 'const p = new Proxy({}, {\n  get(t, k) { return k in t ? t[k] : "missing"; }\n});', "Proxies intercept get/set traps."),
        ("eventloop", "Event Loop", 'console.log("1");\nsetTimeout(() => console.log("2"), 0);\nPromise.resolve().then(() => console.log("3"));\n// 1, 3, 2', "Microtasks run before macrotasks."),
        ("perf", "Memoization", 'const memo = (fn) => {\n  const cache = new Map();\n  return (n) => cache.has(n) ? cache.get(n) : cache.set(n, fn(n)).get(n);\n};', "Memoization caches results."),
    ],
)


LANGS["typescript"] = dict(
    emoji="\U0001f4d1", name="TypeScript",
    playground='<a href="https://www.typescriptlang.org/play" target="_blank" rel="noopener">TS Playground</a>',
    what="<p>TypeScript is <strong>JavaScript with types</strong>. It catches errors before you run the code and gives great editor support. Compiles to plain JS.</p><ul><li>Large web apps (Angular, NestJS)</li><li>Frontend with React/Vue + strict typing</li><li>Node.js backends</li><li>Anywhere JS runs, safer</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'let msg: string = "Hello, world!";\nconsole.log(msg);', "Types are declared with <code>: type</code>."),
        ("vars", "Variables & Types", 'let age: number = 36;\nlet isStudent: boolean = true;\nlet name: string = "Ada";', "Primitive types: <code>string</code>, <code>number</code>, <code>boolean</code>."),
        ("control", "If / Else", 'const age = 18;\nif (age >= 18) {\n  console.log("Vote");\n} else {\n  console.log("Too young");\n}', "Same syntax as JS, but type-checked."),
        ("loops", "Loops", 'for (let i = 0; i < 5; i++) console.log(i);', "Loops identical to JS; types inferred."),
        ("functions", "Functions with Types", 'function greet(name: string): string {\n  return `Hello, ${name}!`;\n}', "Parameters and return types are annotated."),
        ("arrays", "Arrays & Tuples", 'let nums: number[] = [1, 2, 3];\nlet pair: [string, number] = ["Ada", 36];', "Typed arrays and fixed-shape tuples."),
    ],
    intermediate=[
        ("interfaces", "Interfaces", 'interface Person {\n  name: string;\n  age: number;\n}\nconst p: Person = { name: "Ada", age: 36 };', "Interfaces describe object shapes."),
        ("generics", "Generics", 'function first<T>(arr: T[]): T {\n  return arr[0];\n}\nfirst<number>([1, 2, 3]);', "Generics make functions reusable &amp; safe."),
        ("unions", "Union & Literal Types", 'type Status = "ok" | "error";\nlet s: Status = "ok";', "Unions narrow possible values."),
        ("modules", "Modules", '// math.ts\nexport function add(a: number, b: number): number {\n  return a + b;\n}', "Same <code>import</code>/<code>export</code> as ES modules."),
        ("classes", "Classes", 'class Animal {\n  constructor(public name: string) {}\n  speak(): string { return this.name; }\n}', "<code>public</code> auto-creates a field."),
    ],
    advanced=[
        ("utility", "Utility Types", 'type PartialUser = Partial<{ name: string; age: number }>;', "Mapped/conditional types like <code>Partial</code>, <code>Pick</code>."),
        ("decorators", "Decorators", 'function Log(target: any, key: string) {\n  console.log(key);\n}\nclass C { @Log method() {} }', "Decorators annotate classes/methods."),
        ("typeguards", "Type Guards", 'function isStr(x: unknown): x is string {\n  return typeof x === "string";\n}', "<code>x is T</code> narrows types in conditions."),
        ("infer", "Conditional & infer", 'type ElementType<T> = T extends (infer E)[] ? E : never;', "Advanced type-level programming."),
    ],
)


LANGS["java"] = dict(
    emoji="\u2615", name="Java",
    playground='<a href="https://replit.com/languages/java" target="_blank" rel="noopener">Replit Java</a> | <a href="https://www.jdoodle.com" target="_blank" rel="noopener">JDoodle</a>',
    what="<p>Java is a <strong>statically-typed, object-oriented</strong> language that runs on the JVM. Write once, run anywhere. Used in enterprise, Android, and big systems.</p><ul><li>Android apps</li><li>Enterprise backends (Spring)</li><li>Big data (Hadoop, Spark)</li><li>Cross-platform tools</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'public class Main {\n  public static void main(String[] args) {\n    System.out.println("Hello, world!");\n  }\n}', "Execution starts in <code>main</code>."),
        ("vars", "Variables & Types", 'int age = 36;\ndouble height = 1.78;\nboolean isStudent = true;\nString name = "Ada";', "Types are explicit: <code>int</code>, <code>double</code>, <code>boolean</code>, <code>String</code>."),
        ("control", "If / Else", 'int age = 18;\nif (age >= 18) System.out.println("Vote");\nelse System.out.println("Too young");', "Curly braces group statements."),
        ("loops", "Loops", 'for (int i = 0; i < 5; i++) System.out.println(i);\nint n = 3;\nwhile (n-- > 0) System.out.println(n);', "Same loop styles as C-style languages."),
        ("functions", "Methods", 'static int add(int a, int b) {\n  return a + b;\n}', "Functions inside classes are called methods."),
        ("arrays", "Arrays & Lists", 'String[] fruits = {"apple", "banana"};\njava.util.List<String> list = new java.util.ArrayList<>();', "Prefer <code>List</code> over raw arrays."),
    ],
    intermediate=[
        ("classes", "Classes & Objects", 'class Person {\n  String name;\n  Person(String n) { name = n; }\n}', "Encapsulate data in classes."),
        ("oop", "OOP Principles", 'interface Animal { void speak(); }\nclass Dog implements Animal {\n  public void speak() { System.out.println("Woof"); }\n}', "Use <code>interface</code> and <code>implements</code>."),
        ("exceptions", "Exceptions", 'try {\n  int x = 1 / 0;\n} catch (ArithmeticException e) {\n  System.out.println("No divide by zero");\n}', "Catch errors with <code>try/catch</code>."),
        ("collections", "Collections", 'java.util.Map<String, Integer> m = new java.util.HashMap<>();\nm.put("Ada", 36);', "Use <code>Map</code>, <code>Set</code>, <code>List</code>."),
        ("streams", "Streams", 'List<Integer> nums = List.of(1,2,3,4);\nlong even = nums.stream().filter(n -> n % 2 == 0).count();', "Functional pipelines with streams."),
    ],
    advanced=[
        ("generics", "Generics", 'class Box<T> {\n  T value;\n  Box(T v) { value = v; }\n}', "Parameterize types safely."),
        ("lambda", "Lambdas", 'Runnable r = () -> System.out.println("Hi");\nnew Thread(r).start();', "Lambdas are anonymous functions."),
        ("records", "Records (Java 16+)", 'record Point(int x, int y) {}\nPoint p = new Point(1, 2);', "Compact immutable data classes."),
        ("concurrency", "Concurrency", 'ExecutorService ex = Executors.newFixedThreadPool(2);\nex.submit(() -> System.out.println("Task"));', "Use executors, not raw threads."),
    ],
)


LANGS["c"] = dict(
    emoji="\U0001f35a", name="C",
    playground='<a href="https://replit.com/languages/c" target="_blank" rel="noopener">Replit C</a> | <a href="https://www.jdoodle.com" target="_blank" rel="noopener">JDoodle</a>',
    what="<p>C is a <strong>low-level, fast</strong> systems language. It powers operating systems, embedded devices, and is the foundation of many modern languages.</p><ul><li>Operating systems (Linux, Windows kernels)</li><li>Embedded &amp; IoT</li><li>Game engines &amp; drivers</li><li>Performance-critical code</li></ul>",
    beginner=[
        ("hello", "Your First Program", '#include <stdio.h>\nint main() {\n  printf("Hello, world!\\n");\n  return 0;\n}', "Programs start in <code>main()</code>."),
        ("vars", "Variables & Types", 'int age = 36;\nfloat height = 1.78f;\ndouble big = 3.14;\nchar c = \'A\';', "Static types: <code>int</code>, <code>float</code>, <code>char</code>."),
        ("control", "If / Else", 'int age = 18;\nif (age >= 18) printf("Vote\\n");\nelse printf("Too young\\n");', "No <code>bool</code> keyword in C89; use 0/1."),
        ("loops", "Loops", 'for (int i = 0; i < 5; i++) printf("%d\\n", i);\nint n = 3;\nwhile (n-- > 0) printf("%d\\n", n);', "Classic C-style loops."),
        ("functions", "Functions", 'int add(int a, int b) {\n  return a + b;\n}', "Declare before use or provide a prototype."),
        ("pointers", "Pointers Intro", 'int x = 10;\nint *p = &x;\nprintf("%d\\n", *p);', "<code>&amp;</code> gets address, <code>*</code> dereferences."),
    ],
    intermediate=[
        ("arrays", "Arrays", 'int nums[5] = {1, 2, 3, 4, 5};\nfor (int i = 0; i < 5; i++) printf("%d\\n", nums[i]);', "Arrays decay to pointers when passed."),
        ("strings", "Strings", 'char name[] = "Ada";\nprintf("%s\\n", name);', "Strings are <code>char</code> arrays ending in <code>\\0</code>."),
        ("structs", "Structs", 'struct Person { char name[20]; int age; };\nstruct Person p = {"Ada", 36};', "Group related data in structs."),
        ("memory", "Dynamic Memory", 'int *arr = malloc(5 * sizeof(int));\narr[0] = 1;\nfree(arr);', "Always <code>free()</code> what you <code>malloc()</code>."),
        ("fileio", "File I/O", 'FILE *f = fopen("a.txt", "w");\nfprintf(f, "Hi");\nfclose(f);', "Use <code>fopen</code>/<code>fclose</code>."),
    ],
    advanced=[
        ("funcptr", "Function Pointers", 'int (*op)(int,int) = add;\nprintf("%d\\n", op(2,3));', "Pointers to functions enable callbacks."),
        ("preproc", "Preprocessor", '#define MAX 100\n#ifdef DEBUG\n  printf("debug\\n");\n#endif', "Macros and conditional compilation."),
        ("bitwise", "Bitwise Ops", 'int flags = 1 | 4;\nif (flags & 1) printf("bit0\\n");', "Manipulate individual bits."),
        ("union", "Unions", 'union Data { int i; float f; };\nunion Data d; d.i = 10;', "Share memory between members."),
    ],
)


LANGS["cpp"] = dict(
    emoji="\U0001f6e1", name="C++",
    playground='<a href="https://replit.com/languages/cpp" target="_blank" rel="noopener">Replit C++</a> | <a href="https://www.jdoodle.com" target="_blank" rel="noopener">JDoodle</a>',
    what="<p>C++ adds <strong>classes, templates, and STL</strong> on top of C. It's used where speed and control matter: games, finance, robotics.</p><ul><li>Game engines (Unreal)</li><li>High-frequency trading</li><li>Operating systems &amp; browsers</li><li>Embedded systems</li></ul>",
    beginner=[
        ("hello", "Your First Program", '#include <iostream>\nint main() {\n  std::cout << "Hello, world!" << std::endl;\n  return 0;\n}', "Use <code>std::cout</code> for output."),
        ("vars", "Variables & Types", 'int age = 36;\ndouble height = 1.78;\nbool isStudent = true;\nstd::string name = "Ada";', "C++ adds <code>std::string</code> and <code>bool</code>."),
        ("control", "If / Else", 'int age = 18;\nif (age >= 18) std::cout << "Vote\\n";\nelse std::cout << "Too young\\n";', "Same control flow as C."),
        ("loops", "Loops", 'for (int i = 0; i < 5; i++) std::cout << i << "\\n";', "Range-based: <code>for (auto x : vec)</code>."),
        ("functions", "Functions", 'int add(int a, int b) {\n  return a + b;\n}', "Overloading allowed by signature."),
        ("classes", "Classes", 'class Person {\npublic:\n  std::string name;\n  int age;\n};', "Encapsulate with <code>public</code>/<code>private</code>."),
    ],
    intermediate=[
        ("stl", "STL Containers", '#include <vector>\nstd::vector<int> v = {1, 2, 3};\nv.push_back(4);', "Use <code>vector</code>, <code>map</code>, <code>set</code>."),
        ("templates", "Templates", 'template<typename T>\nT max(T a, T b) { return a > b ? a : b; }', "Build generic code."),
        ("refs", "References", 'int x = 5;\nint &r = x;\nr = 10;\n// x is now 10', "References are aliases, safer than pointers."),
        ("raii", "RAII", '{\n  std::vector<int> v(1000);\n} // automatically freed', "Resources freed by destructors."),
        ("oop", "Inheritance", 'class Animal { public: virtual void speak() = 0; };\nclass Dog : public Animal { void speak() override {} };', "Polymorphism via virtual methods."),
    ],
    advanced=[
        ("lambdas", "Lambdas", 'auto sum = [](int a, int b) { return a + b; };\nstd::cout << sum(2, 3);', "Inline anonymous functions."),
        ("smartptr", "Smart Pointers", '#include <memory>\nauto p = std::make_unique<int>(5);', "Automatic memory management."),
        ("move", "Move Semantics", 'std::vector<int> a = {1,2,3};\nstd::vector<int> b = std::move(a);', "Avoid costly copies."),
        ("concurrency", "Concurrency", '#include <thread>\nstd::thread t([](){ /* work */ });\nt.join();', "Spawn threads with <code>std::thread</code>."),
    ],
)


LANGS["csharp"] = dict(
    emoji="\U0001f514", name="C#",
    playground='<a href="https://replit.com/languages/csharp" target="_blank" rel="noopener">Replit C#</a> | <a href="https://dotnetfiddle.net" target="_blank" rel="noopener">.NET Fiddle</a>',
    what="<p>C# is a <strong>modern, object-oriented</strong> language by Microsoft on .NET. Great for desktop, web (ASP.NET), games (Unity), and cloud.</p><ul><li>Web APIs (ASP.NET Core)</li><li>Games (Unity)</li><li>Desktop (WPF, MAUI)</li><li>Cloud services</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'using System;\nclass Program {\n  static void Main() {\n    Console.WriteLine("Hello, world!");\n  }\n}', "Entry point is <code>Main()</code>."),
        ("vars", "Variables & Types", 'int age = 36;\ndouble height = 1.78;\nbool isStudent = true;\nstring name = "Ada";', "Types: <code>int</code>, <code>double</code>, <code>bool</code>, <code>string</code>."),
        ("control", "If / Else", 'int age = 18;\nif (age >= 18) Console.WriteLine("Vote");\nelse Console.WriteLine("Too young");', "Curly braces group statements."),
        ("loops", "Loops", 'for (int i = 0; i < 5; i++) Console.WriteLine(i);', "Also <code>foreach</code> for collections."),
        ("functions", "Methods", 'static int Add(int a, int b) => a + b;', "Expression-bodied methods are concise."),
        ("arrays", "Arrays & Lists", 'string[] fruits = {"apple", "banana"};\nvar list = new List<int> { 1, 2, 3 };', "Prefer <code>List&lt;T&gt;</code> over arrays."),
    ],
    intermediate=[
        ("classes", "Classes & Objects", 'class Person {\n  public string Name { get; set; }\n  public int Age;\n}', "Properties use <code>get; set;</code>."),
        ("oop", "OOP", 'interface IAnimal { void Speak(); }\nclass Dog : IAnimal { public void Speak() {} }', "Inheritance &amp; interfaces."),
        ("linq", "LINQ", 'var nums = new[] {1,2,3,4};\nvar even = nums.Where(n => n % 2 == 0);', "Query collections declaratively."),
        ("async", "async/await", 'async Task<string> Load() {\n  using var c = new HttpClient();\n  return await c.GetStringAsync("url");\n}', "Await async operations."),
        ("exceptions", "Exceptions", 'try { int x = 1/0; }\ncatch (DivideByZeroException) { }', "Use <code>try/catch</code>."),
    ],
    advanced=[
        ("generics", "Generics", 'class Box<T> {\n  public T Value { get; set; }\n}', "Type-safe containers."),
        ("records", "Records", 'record Point(int X, int Y);\nvar p = new Point(1, 2);', "Immutable value types."),
        ("pattern", "Pattern Matching", 'string msg = o switch {\n  int i => $"int {i}",\n  _ => "other"\n};', "Powerful <code>switch</code> expressions."),
        ("tasks", "Task Parallelism", 'Parallel.For(0, 10, i => Console.WriteLine(i));', "Data parallelism with TPL."),
    ],
)


LANGS["php"] = dict(
    emoji="\U0001f41b", name="PHP",
    playground='<a href="https://replit.com/languages/php" target="_blank" rel="noopener">Replit PHP</a> | <a href="https://www.jdoodle.com" target="_blank" rel="noopener">JDoodle</a>',
    what="<p>PHP is a <strong>server-side scripting</strong> language built for the web. It powers WordPress, Laravel, and ~75% of websites with a backend.</p><ul><li>Web backends &amp; CMS (WordPress)</li><li>APIs (Laravel, Symfony)</li><li>Dynamic page generation</li><li>Quick prototyping</li></ul>",
    beginner=[
        ("hello", "Your First Program", '<?php\necho "Hello, world!";\n?>', "PHP code goes inside <code>&lt;?php ?&gt;</code>."),
        ("vars", "Variables", '$name = "Ada";\n$age = 36;\n$height = 1.78;\n$isStudent = true;', "Variables start with <code>$</code>."),
        ("control", "If / Else", '$age = 18;\nif ($age >= 18) echo "Vote";\nelse echo "Too young";', "Use <code>elseif</code> for chains."),
        ("loops", "Loops", 'for ($i = 0; $i < 5; $i++) echo $i;\nforeach ([1,2,3] as $n) echo $n;', "<code>foreach</code> is great for arrays."),
        ("functions", "Functions", 'function greet($name) {\n  return "Hello, $name!";\n}', "Strings interpolate variables directly."),
        ("arrays", "Arrays", '$fruits = ["apple", "banana"];\n$fruits[] = "cherry";\n$person = ["name" => "Ada", "age" => 36];', "Arrays are ordered maps in PHP."),
    ],
    intermediate=[
        ("forms", "Forms & GET/POST", 'if ($_SERVER["REQUEST_METHOD"] === "POST") {\n  echo $_POST["name"];\n}', "Read input via <code>$_GET</code>/<code>$_POST</code>."),
        ("classes", "Classes", 'class Person {\n  public $name;\n  function __construct($n) { $this->name = $n; }\n}', "Use <code>$this</code> for instance."),
        ("pdo", "Database (PDO)", '$pdo = new PDO($dsn, $u, $p);\n$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");\n$stmt->execute([1]);', "Always prepare statements (SQL injection)."),
        ("namespaces", "Namespaces", 'namespace App\\Models;\nclass User {}', "Organize code in namespaces."),
        ("composer", "Composer", '{\n  "require": { "monolog/monolog": "^3.0" }\n}', "PHP dependency manager."),
    ],
    advanced=[
        ("traits", "Traits", 'trait Logger { function log($m) { echo $m; } }\nclass A { use Logger; }', "Reuse methods across classes."),
        ("closures", "Closures", '$fn = function($x) { return $x * 2; };\necho $fn(5);', "Anonymous functions with <code>use</code>."),
        ("generators", "Generators", 'function nums() { for ($i=0;;$i++) yield $i; }', "Lazy iteration with <code>yield</code>."),
        ("attributes", "Attributes (PHP 8)", '#[Route("/home")]\nclass HomeController {}', "Native annotations via attributes."),
    ],
)

LANGS["ruby"] = dict(
    emoji="\U0001f48e", name="Ruby",
    playground='<a href="https://replit.com/languages/ruby" target="_blank" rel="noopener">Replit Ruby</a> | <a href="https://www.jdoodle.com" target="_blank" rel="noopener">JDoodle</a>',
    what="<p>Ruby is a <strong>elegant, object-oriented</strong> language focused on developer happiness. Famous for the Rails web framework.</p><ul><li>Web apps (Ruby on Rails)</li><li>Scripts &amp; automation</li><li>Prototyping</li><li>Dev tooling</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'puts "Hello, world!"', "<code>puts</code> prints with a newline."),
        ("vars", "Variables", 'name = "Ada"\nage = 36\nheight = 1.78\nis_student = true', "Dynamic typing, no declarations."),
        ("control", "If / Else", 'age = 18\nif age >= 18\n  puts "Vote"\nelse\n  puts "Too young"\nend', "Blocks end with <code>end</code>."),
        ("loops", "Loops", '5.times { |i| puts i }\n(0...3).each { |n| puts n }', "Idiomatic iteration with blocks."),
        ("functions", "Methods", 'def greet(name)\n  "Hello, #{name}!"\nend\nputs greet("World")', "String interpolation with <code>#{}</code>."),
        ("arrays", "Arrays & Hashes", 'fruits = ["apple", "banana"]\nfruits << "cherry"\nperson = { name: "Ada", age: 36 }', "Hashes are key-value stores."),
    ],
    intermediate=[
        ("blocks", "Blocks & Procs", 'double = Proc.new { |x| x * 2 }\nputs double.call(5)', "Closures via blocks/procs/lambdas."),
        ("classes", "Classes", 'class Person\n  attr_accessor :name\n  def initialize(n); @name = n; end\nend', "Instance vars start with <code>@</code>."),
        ("modules", "Modules & Mixins", 'module Greetable\n  def greet; "hi"; end\nend\nclass User; include Greetable; end', "Mixins add shared behavior."),
        ("enums", "Enumerables", 'nums = [1,2,3,4]\nputs nums.select { |n| n.even? }', "Rich Enumerable methods."),
        ("files", "File I/O", 'File.write("a.txt", "Hi")\nputs File.read("a.txt")', "Simple file helpers."),
    ],
    advanced=[
        ("metaprog", "Metaprogramming", 'class Foo\n  define_method(:bar) { "baz" }\nend', "Define methods at runtime."),
        ("symbols", "Symbols", 'h = { name: "Ada" }\nh[:name]', "Symbols are immutable identifiers."),
        ("exception", "Exceptions", 'begin\n  raise "oops"\nrescue => e\n  puts e.message\nend', "Use <code>begin/rescue</code>."),
        ("gem", "Gems & Bundler", 'gem "rails", "7.0"\n# bundle install', "Ruby's package ecosystem."),
    ],
)


LANGS["go"] = dict(
    emoji="\U0001f433", name="Go",
    playground='<a href="https://go.dev/play" target="_blank" rel="noopener">Go Playground</a>',
    what="<p>Go (Golang) is a <strong>fast, statically-typed</strong> language by Google. Built for concurrency and cloud infrastructure.</p><ul><li>Cloud services &amp; microservices</li><li>DevOps tooling (Docker, Kubernetes)</li><li>High-performance APIs</li><li>CLI tools</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'package main\nimport "fmt"\nfunc main() {\n  fmt.Println("Hello, world!")\n}', "Every program has <code>package main</code>."),
        ("vars", "Variables & Types", 'var age int = 36\nheight := 1.78\nname := "Ada"\nisStudent := true', "Use <code>:=</code> for short declaration."),
        ("control", "If / Else", 'if age := 18; age >= 18 {\n  fmt.Println("Vote")\n} else {\n  fmt.Println("Too young")\n}', "If can include an init statement."),
        ("loops", "Loops", 'for i := 0; i < 5; i++ {\n  fmt.Println(i)\n}', "Go has only <code>for</code> loops."),
        ("functions", "Functions", 'func add(a int, b int) int {\n  return a + b\n}', "Types come after names."),
        ("slices", "Slices & Maps", 'fruits := []string{"apple", "banana"}\nfruits = append(fruits, "cherry")\nm := map[string]int{"Ada": 36}', "Slices are dynamic; maps are built-in."),
    ],
    intermediate=[
        ("structs", "Structs", 'type Person struct {\n  Name string\n  Age  int\n}\np := Person{"Ada", 36}', "Group fields in structs."),
        ("methods", "Methods", 'func (p Person) Greet() string {\n  return "Hi " + p.Name\n}', "Methods have a receiver."),
        ("interfaces", "Interfaces", 'type Stringer interface { String() string }\n// satisfied implicitly', "Duck typing via interfaces."),
        ("errors", "Error Handling", 'f, err := os.Open("a.txt")\nif err != nil {\n  log.Fatal(err)\n}', "Errors are values, checked explicitly."),
        ("packages", "Packages", 'import (\n  "fmt"\n  "os"\n)', "Group imports in parentheses."),
    ],
    advanced=[
        ("goroutines", "Goroutines", 'go func() {\n  fmt.Println("async")\n}()', "Lightweight threads via <code>go</code>."),
        ("channels", "Channels", 'ch := make(chan int)\ngo func() { ch <- 1 }()\nfmt.Println(<-ch)', "Communicate via channels."),
        ("sync", "Sync & Mutex", 'var mu sync.Mutex\nmu.Lock()\n// critical section\nmu.Unlock()', "Protect shared state."),
        ("generics", "Generics (Go 1.18+)", 'func Map[T any](s []T, f func(T) T) []T { return s }', "Type parameters with <code>any</code>."),
    ],
)

LANGS["rust"] = dict(
    emoji="\U0001f9f0", name="Rust",
    playground='<a href="https://play.rust-lang.org" target="_blank" rel="noopener">Rust Playground</a>',
    what="<p>Rust is a <strong>memory-safe, systems</strong> language without a garbage collector. It prevents bugs at compile time and is blazingly fast.</p><ul><li>Systems &amp; OS development</li><li>WebAssembly</li><li>Performance-critical services</li><li>Embedded</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'fn main() {\n  println!("Hello, world!");\n}', "Programs start in <code>fn main()</code>."),
        ("vars", "Variables & Types", 'let age: u32 = 36;\nlet height = 1.78;\nlet name = "Ada";\nlet is_student = true;', "Variables immutable by default; use <code>mut</code>."),
        ("control", "If / Else", 'let age = 18;\nif age >= 18 {\n  println!("Vote");\n} else {\n  println!("Too young");\n}', "If is an expression (returns a value)."),
        ("loops", "Loops", 'for i in 0..5 {\n  println!("{i}");\n}\nlet mut n = 3;\nwhile n > 0 { n -= 1; }', "Ranges with <code>0..5</code>."),
        ("functions", "Functions", 'fn add(a: i32, b: i32) -> i32 {\n  a + b\n}', "Return type after <code>-&gt;</code>; last expr returned."),
        ("collections", "Vectors & HashMaps", 'let mut v = vec![1, 2, 3];\nv.push(4);\nuse std::collections::HashMap;', "Ownership applies; use <code>mut</code> to change."),
    ],
    intermediate=[
        ("ownership", "Ownership", 'let s = String::from("hi");\nlet t = s; // s moved\n// s no longer usable', "Each value has one owner."),
        ("borrowing", "Borrowing", 'fn len(s: &String) -> usize { s.len() }\nlet s = String::from("hi");\nlet l = len(&s);', "Borrow with <code>&amp;</code>, no move."),
        ("structs", "Structs", 'struct Person { name: String, age: u32 }\nimpl Person {\n  fn greet(&self) {}\n}', "Implement methods with <code>impl</code>."),
        ("traits", "Traits", 'trait Animal { fn speak(&self); }\nstruct Dog;\nimpl Animal for Dog { fn speak(&self) {} }', "Traits are interfaces."),
        ("enums", "Enums & Match", 'enum Color { Red, Green }\nlet c = Color::Red;\nmatch c { Color::Red => println!("red"), _ => {} }', "Exhaustive <code>match</code>."),
    ],
    advanced=[
        ("result", "Result & Option", 'let x: Result<i32, &str> = Ok(5);\nlet y = x.unwrap_or(0);', "No exceptions; use <code>Result</code>/<code>Option</code>."),
        ("lifetimes", "Lifetimes", 'fn longest<\'a>(x: &\'a str, y: &\'a str) -> &\'a str { if x.len() > y.len() { x } else { y } }', "Track references' validity."),
        ("closures", "Closures", 'let add = |a: i32, b: i32| a + b;\nprintln!("{}", add(2, 3));', "Capturing anonymous functions."),
        ("async", "Async", 'async fn fetch() -> String {\n  "data".to_string()\n}', "Async via <code>tokio</code>/<code>async-std</code>."),
    ],
)


LANGS["kotlin"] = dict(
    emoji="\U0001f430", name="Kotlin",
    playground='<a href="https://play.kotlinlang.org" target="_blank" rel="noopener">Kotlin Playground</a>',
    what="<p>Kotlin is a <strong>modern, concise</strong> language on the JVM, fully interoperable with Java. Official language for Android.</p><ul><li>Android apps</li><li>Backend (Ktor, Spring)</li><li>Multiplatform (KMM)</li><li>Scripting</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'fun main() {\n  println("Hello, world!")\n}', "Top-level <code>fun main()</code>."),
        ("vars", "Variables", 'val name = "Ada"\nvar age = 36\nval height = 1.78', "Prefer <code>val</code> over <code>var</code>."),
        ("control", "If / Else", 'val age = 18\nval msg = if (age >= 18) "Vote" else "Too young"\nprintln(msg)', "If is an expression."),
        ("loops", "Loops", 'for (i in 0..5) println(i)\nfor (n in list) println(n)', "Ranges with <code>0..5</code> (exclusive end)."),
        ("functions", "Functions", 'fun greet(name: String): String = "Hello, $name!"', "Expression-bodied functions."),
        ("null", "Null Safety", 'var s: String? = null\ns?.length\nval len = s?.length ?: 0', "<code>?</code> marks nullable types."),
    ],
    intermediate=[
        ("classes", "Classes & Data", 'data class Person(val name: String, val age: Int)', "Data classes auto-generate methods."),
        ("oop", "OOP", 'interface Animal { fun speak() }\nclass Dog : Animal { override fun speak() {} }', "Inheritance with <code>:</code>."),
        ("collections", "Collections", 'val nums = listOf(1, 2, 3)\nval even = nums.filter { it % 2 == 0 }', "Functional collection ops."),
        ("lambdas", "Lambdas", 'val add: (Int, Int) -> Int = { a, b -> a + b }', "First-class functions."),
        ("scope", "Scope Functions", 'val p = Person("Ada", 36).apply { println(name) }', "<code>let</code>, <code>run</code>, <code>apply</code>."),
    ],
    advanced=[
        ("coroutines", "Coroutines", 'suspend fun load(): String { delay(100); return "x" }\nlaunch { val d = load() }', "Lightweight concurrency."),
        ("generics", "Generics", 'class Box<T>(val value: T)', "Type parameters."),
        ("sealed", "Sealed Classes", 'sealed class Result { data class Ok(val v: Int): Result()\n  object Err: Result() }', "Restricted hierarchies for <code>when</code>."),
        ("delegation", "Delegation", 'interface Base { fun f() }\nclass Impl : Base { override fun f() {} }\nclass Wrapper(b: Base) : Base by b', "Class delegation via <code>by</code>."),
    ],
)

LANGS["swift"] = dict(
    emoji="\U0001f98b", name="Swift",
    playground='<a href="https://www.swift.org/playgrounds" target="_blank" rel="noopener">Swift Playgrounds</a> | <a href="https://replit.com/languages/swift" target="_blank" rel="noopener">Replit Swift</a>',
    what="<p>Swift is Apple's <strong>fast, safe</strong> language for iOS, macOS, and server-side. Modern syntax with strong type safety.</p><ul><li>iOS &amp; macOS apps</li><li>Server (Vapor)</li><li>Systems scripting</li><li>ML with Core ML</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'print("Hello, world!")', "No <code>main</code> needed in a playground."),
        ("vars", "Variables & Types", 'let name = "Ada"\nvar age = 36\nlet height: Double = 1.78', "Use <code>let</code> (constant) by default."),
        ("control", "If / Else", 'let age = 18\nif age >= 18 {\n  print("Vote")\n} else {\n  print("Too young")\n}', "Conditionals don't need parens."),
        ("loops", "Loops", 'for i in 0..<5 { print(i) }\nfor fruit in ["apple", "banana"] { print(fruit) }', "Use <code>0..&lt;5</code> (half-open)."),
        ("functions", "Functions", 'func greet(_ name: String) -> String {\n  return "Hello, \\(name)!"\n}', "String interpolation with <code>\\()</code>."),
        ("optionals", "Optionals", 'var s: String? = nil\nif let val = s { print(val) }\nprint(s?.count ?? 0)', "<code>?</code> marks optional; unwrap safely."),
    ],
    intermediate=[
        ("structs", "Structs & Classes", 'struct Person {\n  var name: String\n  var age: Int\n}', "Value types (struct) vs reference (class)."),
        ("protocols", "Protocols", 'protocol Animal { func speak() }\nstruct Dog: Animal { func speak() {} }', "Protocols are interfaces."),
        ("closures", "Closures", 'let add: (Int, Int) -> Int = { $0 + $1 }\nprint(add(2, 3))', "Trailing closures &amp; shorthands."),
        ("enums", "Enums", 'enum Direction { case north, south }\nlet d = Direction.north\nswitch d { case .north: break; default: break }', "Powerful enums with associated values."),
        ("collections", "Collections", 'let nums = [1, 2, 3]\nlet even = nums.filter { $0 % 2 == 0 }', "Functional methods on collections."),
    ],
    advanced=[
        ("async", "async/await", 'func load() async -> String {\n  try? await Task.sleep(nanoseconds: 1_000_000_000)\n  return "x"\n}', "Swift Concurrency model."),
        ("generics", "Generics", 'func first<T>(_ arr: [T]) -> T? { arr.first }', "Type parameters."),
        ("property", "Property Wrappers", '@propertyWrapper\nstruct Clamped { var wrappedValue: Int { didSet { } } }', "Reusable property logic."),
        ("actors", "Actors", 'actor Bank {\n  var balance = 0\n  func deposit(_ n: Int) { balance += n }\n}', "Data-race safety for concurrency."),
    ],
)

LANGS["dart"] = dict(
    emoji="\U0001f9b2", name="Dart",
    playground='<a href="https://dartpad.dev" target="_blank" rel="noopener">DartPad</a>',
    what="<p>Dart is a <strong>client-optimized</strong> language by Google, best known for Flutter (cross-platform UI). Compiles to native or JS.</p><ul><li>Cross-platform apps (Flutter)</li><li>Web frontends</li><li>CLI tools</li><li>Server-side</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'void main() {\n  print("Hello, world!");\n}', "Entry point is <code>main()</code>."),
        ("vars", "Variables & Types", 'var name = "Ada";\nint age = 36;\ndouble height = 1.78;\nbool isStudent = true;', "Use <code>var</code> or explicit types."),
        ("control", "If / Else", 'var age = 18;\nif (age >= 18) {\n  print("Vote");\n} else {\n  print("Too young");\n}', "C-style control flow."),
        ("loops", "Loops", 'for (var i = 0; i < 5; i++) print(i);\nfor (var f in ["a", "b"]) print(f);', "Iterate with <code>for-in</code>."),
        ("functions", "Functions", 'String greet(String name) => "Hello, $name!";', "Arrow <code>=&gt;</code> for one-liners."),
        ("collections", "Lists & Maps", 'var fruits = ["apple", "banana"];\nfruits.add("cherry");\nvar m = {"name": "Ada", "age": 36};', "Lists and maps are built-in."),
    ],
    intermediate=[
        ("classes", "Classes", 'class Person {\n  String name;\n  Person(this.name);\n}', "Constructor shorthand <code>this.name</code>."),
        ("oop", "OOP", 'abstract class Animal { void speak(); }\nclass Dog extends Animal { void speak() {} }', "Inheritance with <code>extends</code>."),
        ("async", "async/await", 'Future<String> load() async {\n  return await Future.value("x");\n}', "Futures are like Promises."),
        ("null", "Null Safety", 'String? name;\nprint(name?.length ?? 0);', "Sound null safety by default."),
        ("collections", "Collection Methods", 'var even = [1,2,3,4].where((n) => n.isEven);', "Functional operations."),
    ],
    advanced=[
        ("mixins", "Mixins", 'mixin Logger { void log() => print("log"); }\nclass A with Logger {}', "Reuse implementations via <code>with</code>."),
        ("generics", "Generics", 'class Box<T> { T? value; }', "Type parameters."),
        ("streams", "Streams", 'Stream<int> nums = Stream.periodic(Duration(seconds: 1), (i) => i);', "Async sequences."),
        ("isolates", "Isolates", 'import "dart:isolate";\n// spawn isolates for parallelism', "Concurrency without shared memory."),
    ],
)

LANGS["scala"] = dict(
    emoji="\u269b", name="Scala",
    playground='<a href="https://scastie.scala-lang.org" target="_blank" rel="noopener">Scastie</a>',
    what="<p>Scala blends <strong>object-oriented and functional</strong> programming on the JVM. Great for data engineering (Spark) and scalable backends.</p><ul><li>Big data (Apache Spark)</li><li>Backend services (Play, Akka)</li><li>Distributed systems</li><li>Functional pipelines</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'object Main {\n  def main(args: Array[String]): Unit =\n    println("Hello, world!")\n}', "Programs live in <code>object</code>s."),
        ("vars", "Variables", 'val name = "Ada"\nvar age = 36', "Prefer <code>val</code>."),
        ("control", "If / Else", 'val age = 18\nval msg = if (age >= 18) "Vote" else "Too young"', "If is an expression."),
        ("loops", "Loops", 'for (i <- 0 until 5) println(i)\n(1 to 3).foreach(println)', "Use <code>until</code> / <code>to</code>."),
        ("functions", "Functions", 'def add(a: Int, b: Int): Int = a + b', "Types after parameter names."),
        ("collections", "Collections", 'val nums = List(1, 2, 3)\nval even = nums.filter(_ % 2 == 0)', "Immutable by default."),
    ],
    intermediate=[
        ("caseclass", "Case Classes", 'case class Person(name: String, age: Int)\nval p = Person("Ada", 36)', "Automatic equality, copy, match."),
        ("pattern", "Pattern Matching", 'x match {\n  case 0 => "zero"\n  case n if n > 0 => "pos"\n  case _ => "neg"\n}', "Exhaustive, powerful matching."),
        ("traits", "Traits", 'trait Animal { def speak(): Unit }\nclass Dog extends Animal { def speak() = () }', "Interfaces with implementations."),
        ("higher", "Higher-Order Functions", 'val apply = (f: Int => Int, x: Int) => f(x)', "Functions as values."),
        ("options", "Option", 'val o: Option[Int] = Some(5)\nval v = o.getOrElse(0)', "No nulls; use <code>Option</code>."),
    ],
    advanced=[
        ("implicits", "Implicits", 'implicit val ord: Ordering[Int] = Ordering[Int]\nList(3,1,2).sorted', "Type-class style resolution."),
        ("futures", "Futures", 'import scala.concurrent.Future\nFuture { expensiveWork() }', "Async computations."),
        ("forcomp", "For-Comprehensions", 'for {\n  a <- optA\n  b <- optB\n} yield a + b', "Chain monadic operations."),
        ("macros", "Macros", 'import scala.quoted.*\ninline def twice(n: Int): Int = ${ }', "Compile-time metaprogramming."),
    ],
)


LANGS["r"] = dict(
    emoji="\U0001f4ca", name="R",
    playground='<a href="https://rdrr.io/snippets" target="_blank" rel="noopener">rdrr.io</a> | <a href="https://replit.com/languages/r" target="_blank">Replit R</a>',
    what="<p>R is a <strong>statistical computing</strong> language beloved by data scientists. Excellent for analysis, visualization, and reporting.</p><ul><li>Data analysis &amp; statistics</li><li>Visualization (ggplot2)</li><li>Academic research</li><li>Reporting (R Markdown)</li></ul>",
    beginner=[
        ("hello", "Your First Program", 'print("Hello, world!")', "Use <code>print()</code> or just type the value."),
        ("vars", "Variables", 'name <- "Ada"\nage <- 36\nheight <- 1.78\nis_student <- TRUE', "Assignment with <code>&lt;-</code>."),
        ("control", "If / Else", 'age <- 18\nif (age >= 18) {\n  print("Vote")\n} else {\n  print("Too young")\n}', "Curly braces group statements."),
        ("loops", "Loops", 'for (i in 1:5) print(i)\nn <- 3\nwhile (n > 0) { print(n); n <- n - 1 }', "Vectors drive iteration."),
        ("functions", "Functions", 'greet <- function(name) {\n  paste("Hello,", name, "!")\n}\ngreet("World")', "Defined with <code>function()</code>."),
        ("vectors", "Vectors & Data Frames", 'v <- c(1, 2, 3)\ndf <- data.frame(name = c("Ada"), age = c(36))', "Vectors are the core data type."),
    ],
    intermediate=[
        ("dplyr", "dplyr", 'library(dplyr)\ndf %>% filter(age > 30) %>% summarise(avg = mean(age))', "Grammar of data manipulation."),
        ("ggplot", "ggplot2", 'library(ggplot2)\nggplot(df, aes(x = age)) + geom_histogram()', "Layered grammar of graphics."),
        ("apply", "apply Family", 'sapply(1:5, function(x) x * 2)', "Vectorized iteration."),
        ("read", "Read Data", 'data <- read.csv("file.csv")\nhead(data)', "Import CSV/Excel/JSON easily."),
        ("formula", "Formulas", 'model <- lm(age ~ height, data = df)\nsummary(model)', "Formula syntax for stats."),
    ],
    advanced=[
        ("purrr", "purrr", 'library(purrr)\nmap(list(1, 2), ~ .x * 2)', "Functional programming toolkit."),
        ("s3", "S3 Objects", 'myobj <- structure(1, class = "myclass")\nprint.myclass <- function(x) cat("val:", x, "\\n")', "R's simplest OO system."),
        ("parallel", "Parallel", 'library(parallel)\nmclapply(1:4, function(x) x^2, mc.cores = 2)', "Parallelize computations."),
        ("shiny", "Shiny", 'library(shiny)\nui <- fluidPage("Hello")\nserver <- function(input, output) {}\nshinyApp(ui, server)', "Build interactive web apps."),
    ],
)

LANGS["sql"] = dict(
    emoji="\U0001f4bf", name="SQL",
    playground='<a href="https://www.db-fiddle.com" target="_blank" rel="noopener">DB Fiddle</a> | <a href="https://sqliteonline.com" target="_blank" rel="noopener">SQLite Online</a>',
    what="<p>SQL is the <strong>language of databases</strong>. It queries, inserts, and manages data in relational systems (PostgreSQL, MySQL, SQLite).</p><ul><li>Backend data storage</li><li>Analytics &amp; reporting</li><li>Data engineering</li><li>Almost every app's backend</li></ul>",
    beginner=[
        ("hello", "Your First Query", 'SELECT "Hello, world!" AS greeting;', "A query returns a result set."),
        ("select", "SELECT & WHERE", 'SELECT name, age\nFROM users\nWHERE age >= 18;', "Filter rows with <code>WHERE</code>."),
        ("insert", "INSERT", "INSERT INTO users (name, age)\nVALUES ('Ada', 36);", "Add new rows."),
        ("update", "UPDATE & DELETE", 'DELETE FROM users\nWHERE age < 0;', "Modify or remove rows carefully."),
        ("order", "ORDER & LIMIT", 'SELECT * FROM users\nORDER BY age DESC\nLIMIT 10;', "Sort and restrict results."),
        ("functions", "Aggregates", 'SELECT COUNT(*), AVG(age)\nFROM users;', "Compute across rows."),
    ],
    intermediate=[
        ("joins", "JOINs", 'SELECT u.name, o.total\nFROM users u\nJOIN orders o ON o.user_id = u.id;', "Combine tables by key."),
        ("group", "GROUP BY", 'SELECT country, COUNT(*)\nFROM users\nGROUP BY country;', "Aggregate per group."),
        ("subquery", "Subqueries", 'SELECT name FROM users\nWHERE age > (SELECT AVG(age) FROM users);', "Queries inside queries."),
        ("cte", "CTEs", 'WITH adults AS (\n  SELECT * FROM users WHERE age >= 18\n)\nSELECT COUNT(*) FROM adults;', "Readable temporary result sets."),
        ("index", "Indexes", 'CREATE INDEX idx_users_age\nON users(age);', "Speed up lookups."),
    ],
    advanced=[
        ("transactions", "Transactions", 'BEGIN;\nUPDATE accounts SET bal = bal - 10 WHERE id = 1;\nUPDATE accounts SET bal = bal + 10 WHERE id = 2;\nCOMMIT;', "Atomic multi-step changes."),
        ("window", "Window Functions", 'SELECT name,\n  RANK() OVER (ORDER BY age DESC) AS r\nFROM users;', "Compute across rows without grouping."),
        ("views", "Views", 'CREATE VIEW v_adults AS\nSELECT * FROM users WHERE age >= 18;', "Reusable virtual tables."),
        ("json", "JSON Support", "SELECT data->>'name'\nFROM events\nWHERE data->>'type' = 'click';", "Query JSON columns."),
    ],
)

# ---- Generate all ----
for lang, d in LANGS.items():
    out = BASE / f"{lang}.html"
    out.write_text(build(lang, d), encoding="utf-8")
    print("Wrote", out.name)

