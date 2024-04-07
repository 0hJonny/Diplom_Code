from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenerationResponse:
    model: str
    created_at: datetime
    response: str
    done: bool
    total_duration: int
    load_duration: int
    prompt_eval_duration: int
    eval_duration: int

    @classmethod
    def from_json(cls, data):
        """
        A constructor method that creates an instance of the class from a dictionary.
        
        Parameters:
            data (dict): A dictionary containing the necessary data to create the instance.
        
        Returns:
            An instance of the class initialized with the data from the dictionary.
        """
        return cls(
            model=data["model"],
            created_at=datetime.fromisoformat(data["created_at"][:26]),
            response=data["response"],
            done=data["done"],
            total_duration=data["total_duration"],
            load_duration=data["load_duration"],
            prompt_eval_duration=data["prompt_eval_duration"],
            eval_duration=data["eval_duration"],
        )

