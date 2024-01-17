// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

const legend = new vscode.SemanticTokensLegend(
    ['keyword', 'number', 'operator', 'oparator', 'string', 'space', 'comment', 'error', 'operator', 'variable', 'function', 'namespace'],
	[]
);
class MyDocumentSemanticTokensProvider {
	constructor() {
		// nothing to do
	}

	provideDocumentSemanticTokens(document) {
		const { spawnSync } = require('child_process');
		let filePath = document.fileName.replace(/\\/g, '\\\\');
		const python = spawnSync('python', ['./analyzer/main.py', '--file', filePath], {cwd: __dirname});
		if (python.error) {
			console.error(`Failed to start subprocess. ${python.error}`);
		}
		else{
			console.log(`child process exited with code ${python.status}`);
			const fs = require('fs');
			const path = require('path');
			const filepath = path.join(__dirname, './colors.pyknights');
			let content = fs.readFileSync(filepath, 'utf8');
			const colors = JSON.parse(content);
			
			const builder = new vscode.SemanticTokensBuilder(legend);
			for (const item of colors) {
				builder.push(
					item.startRow - 1,
					item.startColumn - 1,
					item.endColumn - item.startColumn + 1,
					item.type
				);
			}
			return builder.build();
		}
	}

	provideDocumentRangeSemanticTokens(document, range) {
		// todo: run python code for lexical, syntactic, semantic analysis
	}
}

class MyCompletionItemProvider {
	provideCompletionItems(document, position, token, context) {
		const { spawnSync } = require('child_process');
		let filePath = document.fileName.replace(/\\/g, '\\\\');
		const python = spawnSync('python', ['./analyzer/main.py', '--file', filePath, '--complete', `${position.line},${position.character}`], {cwd: __dirname});

		if (python.error) {
			console.error(`Failed to start subprocess. ${python.error}`);
		} else {
			console.log(`child process exited with code ${python.status}`);
			const fs = require('fs');
			const path = require('path');
			const filepath = path.join(__dirname, './completions.pyknights');
			const completions = JSON.parse(fs.readFileSync(filepath, 'utf8'));
			console.log(completions);
			return completions.map(completion => {
				let item = new vscode.CompletionItem(completion.name, vscode.CompletionItemKind[completion.type]);
				if(completion.type == 'Function' || completion.type == 'Class'){
					item.detail = completion.detail;
				}
				return item;
			});
		}
	}
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This row of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "pyknights" is now active!');

	context.subscriptions.push(vscode.languages.registerDocumentSemanticTokensProvider(
		{ language: 'python' },
		new MyDocumentSemanticTokensProvider(),
		legend
	));

	context.subscriptions.push(vscode.languages.registerCompletionItemProvider(
		{ language: 'python' },
		new MyCompletionItemProvider(),
		'.', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
	));

	vscode.workspace.onDidChangeTextDocument(event => {}, null, context.subscriptions);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate,
	MyDocumentSemanticTokensProvider,
	MyCompletionItemProvider
}
