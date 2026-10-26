from core.workflow import build_workflow

if __name__ == '__main__':
    app = build_workflow()
    request = input('Ask your data engineering question: ').strip()
    if not request:
        raise SystemExit('Please enter a question.')
    result = app.invoke({'user_request': request, 'selected_agent': '', 'result': ''})
    print(f"\nSelected agent: {result['selected_agent']}\n")
    print(result['result'])
