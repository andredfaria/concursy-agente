import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Importações condicionais para diferentes providers
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_community.llms import Ollama
    from langchain_community.chat_models import ChatOllama
except ImportError:
    Ollama = None
    ChatOllama = None

try:
    from langchain_huggingface import HuggingFaceEndpoint
except ImportError:
    HuggingFaceEndpoint = None

# Carregar variáveis do arquivo .env
load_dotenv()

class LLMProvider:
    """Enum-like class para providers de LLM"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROQ = "groq"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"

class LLMConfig:
    """Configurações padrão para diferentes providers"""
    
    DEFAULT_CONFIGS = {
        LLMProvider.OPENAI: {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        LLMProvider.ANTHROPIC: {
            "model": "claude-3-haiku-20240307",
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        LLMProvider.GOOGLE: {
            "model": "gemini-1.5-flash",
            "temperature": 0.7,
            "max_output_tokens": 2000,
        },
        LLMProvider.GROQ: {
            "model": "llama3-8b-8192",
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        LLMProvider.OLLAMA: {
            "model": "llama3.1:8b",
            "temperature": 0.7,
        },
        LLMProvider.HUGGINGFACE: {
            "repo_id": "microsoft/DialoGPT-large",
            "temperature": 0.7,
            "max_length": 2000,
        }
    }

class LLMFactory:
    """Factory class para criar instâncias de diferentes LLMs"""
    
    @staticmethod
    def create_llm(provider: str, custom_config: Optional[Dict[str, Any]] = None):
        """
        Cria uma instância de LLM baseada no provider especificado
        
        Args:
            provider: Nome do provider (openai, anthropic, google, etc.)
            custom_config: Configurações customizadas para sobrescrever as padrões
            
        Returns:
            Instância do LLM configurado
            
        Raises:
            ValueError: Se o provider não for suportado ou se dependências estão faltando
        """
        # Obter configurações padrão
        if provider not in LLMConfig.DEFAULT_CONFIGS:
            raise ValueError(f"Provider '{provider}' não é suportado. "
                           f"Providers disponíveis: {list(LLMConfig.DEFAULT_CONFIGS.keys())}")
        
        config = LLMConfig.DEFAULT_CONFIGS[provider].copy()
        
        # Aplicar configurações customizadas se fornecidas
        if custom_config:
            config.update(custom_config)
        
        # Criar instância baseada no provider
        if provider == LLMProvider.OPENAI:
            return LLMFactory._create_openai_llm(config)
        elif provider == LLMProvider.ANTHROPIC:
            return LLMFactory._create_anthropic_llm(config)
        elif provider == LLMProvider.GOOGLE:
            return LLMFactory._create_google_llm(config)
        elif provider == LLMProvider.GROQ:
            return LLMFactory._create_groq_llm(config)
        elif provider == LLMProvider.OLLAMA:
            return LLMFactory._create_ollama_llm(config)
        elif provider == LLMProvider.HUGGINGFACE:
            return LLMFactory._create_huggingface_llm(config)
        else:
            raise ValueError(f"Provider '{provider}' não implementado")
    
    @staticmethod
    def _create_openai_llm(config: Dict[str, Any]):
        """Cria instância do OpenAI LLM"""
        if ChatOpenAI is None:
            raise ImportError("langchain-openai não está instalado. Execute: pip install langchain-openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada! Configure a chave da OpenAI no arquivo .env")
        
        return ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            openai_api_key=api_key
        )
    
    @staticmethod
    def _create_anthropic_llm(config: Dict[str, Any]):
        """Cria instância do Anthropic LLM"""
        if ChatAnthropic is None:
            raise ImportError("langchain-anthropic não está instalado. Execute: pip install langchain-anthropic")
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY não encontrada! Configure a chave da Anthropic no arquivo .env")
        
        return ChatAnthropic(
            model=config["model"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            anthropic_api_key=api_key
        )
    
    @staticmethod
    def _create_google_llm(config: Dict[str, Any]):
        """Cria instância do Google LLM"""
        if ChatGoogleGenerativeAI is None:
            raise ImportError("langchain-google-genai não está instalado. Execute: pip install langchain-google-genai")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY não encontrada! Configure a chave do Google no arquivo .env")
        
        return ChatGoogleGenerativeAI(
            model=config["model"],
            temperature=config["temperature"],
            max_output_tokens=config["max_output_tokens"],
            google_api_key=api_key
        )
    
    @staticmethod
    def _create_groq_llm(config: Dict[str, Any]):
        """Cria instância do Groq LLM"""
        if ChatGroq is None:
            raise ImportError("langchain-groq não está instalado. Execute: pip install langchain-groq")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY não encontrada! Configure a chave do Groq no arquivo .env")
        
        return ChatGroq(
            model=config["model"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            groq_api_key=api_key
        )
    
    @staticmethod
    def _create_ollama_llm(config: Dict[str, Any]):
        """Cria instância do Ollama LLM (local)"""
        if ChatOllama is None:
            raise ImportError("langchain-community não está instalado. Execute: pip install langchain-community")
        
        # Ollama não precisa de API key, roda localmente
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        return ChatOllama(
            model=config["model"],
            temperature=config["temperature"],
            base_url=base_url
        )
    
    @staticmethod
    def _create_huggingface_llm(config: Dict[str, Any]):
        """Cria instância do HuggingFace LLM"""
        if HuggingFaceEndpoint is None:
            raise ImportError("langchain-huggingface não está instalado. Execute: pip install langchain-huggingface")
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            raise ValueError("❌ HUGGINGFACE_API_KEY não encontrada! Configure a chave do HuggingFace no arquivo .env")
        
        return HuggingFaceEndpoint(
            repo_id=config["repo_id"],
            temperature=config["temperature"],
            max_length=config["max_length"],
            huggingfacehub_api_token=api_key
        )
    
    @staticmethod
    def list_available_providers() -> Dict[str, bool]:
        """
        Lista todos os providers disponíveis e se suas dependências estão instaladas
        
        Returns:
            Dict com provider como chave e True/False se está disponível
        """
        availability = {}
        
        # Verificar disponibilidade de cada provider
        availability[LLMProvider.OPENAI] = ChatOpenAI is not None
        availability[LLMProvider.ANTHROPIC] = ChatAnthropic is not None
        availability[LLMProvider.GOOGLE] = ChatGoogleGenerativeAI is not None
        availability[LLMProvider.GROQ] = ChatGroq is not None
        availability[LLMProvider.OLLAMA] = ChatOllama is not None
        availability[LLMProvider.HUGGINGFACE] = HuggingFaceEndpoint is not None
        
        return availability
    
    @staticmethod
    def get_provider_info() -> Dict[str, Dict[str, Any]]:
        """
        Retorna informações sobre cada provider
        
        Returns:
            Dict com informações detalhadas de cada provider
        """
        return {
            LLMProvider.OPENAI: {
                "name": "OpenAI",
                "description": "GPT-4, GPT-3.5 e outros modelos da OpenAI",
                "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4-turbo"],
                "requires_api_key": True,
                "env_var": "OPENAI_API_KEY",
                "install_command": "pip install langchain-openai"
            },
            LLMProvider.ANTHROPIC: {
                "name": "Anthropic Claude",
                "description": "Modelos Claude da Anthropic",
                "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
                "requires_api_key": True,
                "env_var": "ANTHROPIC_API_KEY",
                "install_command": "pip install langchain-anthropic"
            },
            LLMProvider.GOOGLE: {
                "name": "Google Gemini",
                "description": "Modelos Gemini do Google",
                "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
                "requires_api_key": True,
                "env_var": "GOOGLE_API_KEY",
                "install_command": "pip install langchain-google-genai"
            },
            LLMProvider.GROQ: {
                "name": "Groq",
                "description": "Modelos rápidos via Groq",
                "models": ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
                "requires_api_key": True,
                "env_var": "GROQ_API_KEY",
                "install_command": "pip install langchain-groq"
            },
            LLMProvider.OLLAMA: {
                "name": "Ollama (Local)",
                "description": "Modelos locais via Ollama",
                "models": ["llama3.1:8b", "llama3.1:70b", "codellama", "mistral"],
                "requires_api_key": False,
                "env_var": "OLLAMA_BASE_URL (opcional)",
                "install_command": "pip install langchain-community + instalar Ollama"
            },
            LLMProvider.HUGGINGFACE: {
                "name": "HuggingFace",
                "description": "Modelos do HuggingFace Hub",
                "models": ["microsoft/DialoGPT-large", "facebook/blenderbot-400M-distill"],
                "requires_api_key": True,
                "env_var": "HUGGINGFACE_API_KEY",
                "install_command": "pip install langchain-huggingface"
            }
        } 