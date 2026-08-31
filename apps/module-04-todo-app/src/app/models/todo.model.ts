export type Priority = 'low' | 'medium' | 'high';

export type FilterMode = 'all' | 'active' | 'completed';

export interface Todo {
  readonly id: string;
  title: string;
  completed: boolean;
  priority: Priority;
  readonly createdAt: Date;
}

export interface PriorityOption {
  key: Priority;
  value: string;
}

export type CreateTodoInput = Omit<Todo, 'id' | 'createdAt'>;

export type UpdateTodoInput = Pick<Todo, 'id' | 'title'>;

export function isTodo(obj: unknown): obj is Todo {
  if (typeof obj !== 'object' || obj === null) return false;

  const t = obj as Record<string, unknown>;
  return (
    typeof t['id'] === 'string' &&
    typeof t['title'] === 'string' &&
    typeof t['completed'] === 'boolean' &&
    typeof t['priority'] === 'string' &&
    ['low', 'medium', 'high'].includes(t['priority']) &&
    typeof t['createdAt'] === 'string'
  );
}

export function isTodoArray(arr: unknown): arr is Todo[] {
  return Array.isArray(arr) && arr.every(isTodo);
}
