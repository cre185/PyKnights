// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

const legend = new vscode.SemanticTokensLegend(
    ['reserved', 'constant', 'operator', 'separator', 'string', 'space', 'comment', 'error', 'assigner', 'variable', 'function', 'package'],
    []
);
class MyDocumentSemanticTokensProvider {
	constructor() {
		// nothing to do
	}

	provideDocumentSemanticTokens(document) {
		// run python code for lexical, syntactic, semantic analysis
		// (assume this extention.js is at . )
		// run ./analyzer/main.py
		// it will generate a colors.pyknights file
		// read that file as an array of dicts
		// reinterpret that array to become the data part of SemanticTokens
		// return that SemanticTokens
		// 1. run python code at ./analyzer/main.py
		const { spawnSync } = require('child_process');
		let filePath = document.fileName.replace(/\\/g, '\\\\');
		const python = spawnSync('./analyzer/main.exe', ['--file', filePath], {cwd: __dirname});
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
					item.startLine - 1,
					item.startColumn - 1,
					item.endColumn - item.startColumn + 1,
					item.tokenType,
					[]
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
		const python = spawnSync('./analyzer/main.exe', ['--file', filePath, '--complete', `${position.line},${position.character}`], {cwd: __dirname});

		if (python.error) {
			console.error(`Failed to start subprocess. ${python.error}`);
		} else {
			console.log(`child process exited with code ${python.status}`);
			const fs = require('fs');
			const path = require('path');
			const filepath = path.join(__dirname, './completions.pyknights');
			const completions = JSON.parse(fs.readFileSync(filepath, 'utf8'));
			return completions.map(completion => {
				let item = new vscode.CompletionItem(completion.name, vscode.CompletionItemKind[completion.kind]);
				console.log(item);
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

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('pyknights.helloWorld', function () {
		// The code you place here will be executed every time your command is executed

		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from PyKnights!');
	});

	context.subscriptions.push(disposable);

	context.subscriptions.push(vscode.languages.registerDocumentSemanticTokensProvider(
		{ language: 'python' },
		new MyDocumentSemanticTokensProvider(),
		legend
	));

	context.subscriptions.push(vscode.languages.registerCompletionItemProvider(
		{ language: 'python' },
		new MyCompletionItemProvider(),
		'.'
	));

	vscode.workspace.onDidChangeTextDocument(event => {
        if (event.document.languageId === 'python') {
            console.log('Python code has been edited!');
			// todo: run python code for lexical, syntactic, semantic analysis
        }
    }, null, context.subscriptions);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate,
	MyDocumentSemanticTokensProvider,
	MyCompletionItemProvider
}
