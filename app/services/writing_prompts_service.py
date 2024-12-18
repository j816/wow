from typing import List, Optional, Dict, Set
import os
import random
from pathlib import Path

class WritingPromptsService:
    def __init__(self):
        self._prompt_folder: Optional[Path] = None
        self._shown_prompts: Dict[str, Set[str]] = {}
        self._current_prompts: Dict[str, str] = {}

    def set_prompt_folder(self, folder: str) -> bool:
        if not os.path.exists(folder):
            return False
        
        # Check if the folder has at least one subfolder for categories
        path = Path(folder)
        subfolders = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not subfolders:
            raise ValueError("Selected folder must contain at least one category subfolder")
        
        self._prompt_folder = Path(folder)
        return True
    
    def get_prompt_folder(self) -> Optional[Path]:
        return self._prompt_folder
    
    def get_subfolders(self) -> List[str]:
        if not self._prompt_folder:
            return []
        return [d.name for d in self._prompt_folder.iterdir() if d.is_dir() and not d.name.startswith('.')]

    def get_new_prompt(self, category: str) -> Optional[str]:
        if not self._prompt_folder or not category:
            return None
            
        category_path = self._prompt_folder / category
        if not category_path.exists():
            return None
        
        prompt_files = [f for f in category_path.iterdir()
                        if f.suffix in ['.txt', '.md'] and not f.name.startswith('.')]
        
        if not prompt_files:
            return None
            
        if category not in self._shown_prompts:
            self._shown_prompts[category] = set()
            
        if len(self._shown_prompts[category]) == len(prompt_files):
            self._shown_prompts[category].clear()
        
        unshown_prompts = [f for f in prompt_files if str(f) not in self._shown_prompts[category]]
        
        selected_file = random.choice(unshown_prompts)
        self._shown_prompts[category].add(str(selected_file))
        
        try:
            with open(selected_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read().strip()
                self._current_prompts[category] = prompt_content
                return prompt_content
        except Exception as e:
            print(f"Error reading prompt file: {e}")
            return None
    
    def get_current_prompt(self, category: str) -> Optional[str]:
        """Get the currently displayed prompt for a category."""
        return self._current_prompts.get(category)
    
    def reset_tracking(self, category: Optional[str] = None):
        if category:
            self._shown_prompts.pop(category, None)
            self._current_prompts.pop(category, None)
        else:
            self._shown_prompts.clear()
            self._current_prompts.clear()
