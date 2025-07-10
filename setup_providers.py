#!/usr/bin/env python3
"""
Script utilitário para configurar e testar providers de LLM
"""

import subprocess
import sys
import os
from typing import Dict, List
from llm_config import LLMFactory, LLMProvider

def install_package(package_name: str) -> bool:
    """
    Instala um pacote Python usando pip
    
    Args:
        package_name: Nome do pacote para instalar
        
    Returns:
        True se instalação foi bem-sucedida
    """
    try:
        print(f"📦 Instalando {package_name}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {package_name} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package_name}: {e}")
        return False

def setup_provider_installation():
    """Interface para instalar providers específicos"""
    provider_packages = {
        LLMProvider.ANTHROPIC: "langchain-anthropic",
        LLMProvider.GOOGLE: "langchain-google-genai", 
        LLMProvider.GROQ: "langchain-groq",
        LLMProvider.HUGGINGFACE: "langchain-huggingface"
    }
    
    print("🚀 Instalador de Providers de LLM")
    print("=" * 50)
    
    # Verificar status atual
    factory = LLMFactory()
    available = factory.list_available_providers()
    provider_info = factory.get_provider_info()
    
    print("\n📋 Status atual dos providers:")
    for provider, is_available in available.items():
        status = "✅ Instalado" if is_available else "❌ Não instalado"
        print(f"  {provider_info[provider]['name']}: {status}")
    
    print("\n🎯 Que providers você gostaria de instalar?")
    print("0. Instalar todos os providers opcionais")
    
    options = []
    for i, (provider, package) in enumerate(provider_packages.items(), 1):
        if not available[provider]:
            print(f"{i}. {provider_info[provider]['name']} ({package})")
            options.append((provider, package))
    
    if not options:
        print("✅ Todos os providers opcionais já estão instalados!")
        return
    
    print(f"{len(options) + 1}. Sair")
    
    try:
        choice = input("\n> Escolha uma opção: ").strip()
        
        if choice == "0":
            # Instalar todos
            for provider, package in provider_packages.items():
                if not available[provider]:
                    install_package(package)
        elif choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(options):
                provider, package = options[choice_idx]
                install_package(package)
            elif int(choice) == len(options) + 1:
                print("👋 Saindo...")
                return
            else:
                print("❌ Opção inválida!")
        else:
            print("❌ Digite um número válido!")
            
    except KeyboardInterrupt:
        print("\n👋 Instalação cancelada.")

def test_provider_connection():
    """Testa a conexão com os providers configurados"""
    print("🧪 Testando Providers Configurados")
    print("=" * 50)
    
    factory = LLMFactory()
    available = factory.list_available_providers()
    provider_info = factory.get_provider_info()
    
    for provider, is_available in available.items():
        if not is_available:
            continue
            
        info = provider_info[provider]
        print(f"\n🔍 Testando {info['name']}...")
        
        # Verificar API key se necessário
        if info['requires_api_key']:
            env_var = info['env_var'].split()[0]  # Pegar apenas o nome da variável
            if not os.getenv(env_var):
                print(f"  ❌ API Key não configurada ({env_var})")
                continue
            else:
                print(f"  ✅ API Key configurada")
        
        # Tentar criar instância do LLM
        try:
            llm = factory.create_llm(provider)
            print(f"  ✅ {info['name']} configurado corretamente!")
            
            # Teste básico opcional (comentado para evitar custos)
            # test_message = "Diga apenas 'OK' se você está funcionando."
            # response = llm.invoke(test_message)
            # print(f"  🎯 Resposta de teste: {response.content[:50]}...")
            
        except Exception as e:
            print(f"  ❌ Erro na configuração: {e}")

def show_provider_info():
    """Mostra informações detalhadas sobre todos os providers"""
    print("📖 Informações dos Providers")
    print("=" * 50)
    
    factory = LLMFactory()
    provider_info = factory.get_provider_info()
    available = factory.list_available_providers()
    
    for provider, info in provider_info.items():
        status = "✅ Disponível" if available[provider] else "❌ Não instalado"
        
        print(f"\n🤖 {info['name']} ({provider}) - {status}")
        print(f"   📝 {info['description']}")
        print(f"   🔧 Modelos: {', '.join(info['models'][:3])}...")
        print(f"   🔑 API Key: {'Necessária' if info['requires_api_key'] else 'Não necessária'}")
        if info['requires_api_key']:
            print(f"   🌐 Variável: {info['env_var']}")
        print(f"   📦 Instalar: {info['install_command']}")

def create_env_file():
    """Cria um arquivo .env básico"""
    env_content = """# Configuração básica - edite conforme necessário
OPENAI_API_KEY=sua-chave-openai-aqui

# Descomente e configure conforme necessário:
# PREFERRED_LLM_PROVIDER=openai
# ANTHROPIC_API_KEY=sua-chave-anthropic-aqui
# GOOGLE_API_KEY=sua-chave-google-aqui
# GROQ_API_KEY=sua-chave-groq-aqui
# HUGGINGFACE_API_KEY=sua-chave-huggingface-aqui
# OLLAMA_BASE_URL=http://localhost:11434
"""
    
    if os.path.exists(".env"):
        response = input("❓ Arquivo .env já existe. Sobrescrever? (s/N): ").lower()
        if response != 's':
            print("⏭️ Mantendo arquivo .env existente.")
            return
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Arquivo .env criado! Edite-o com suas API keys.")
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")

def main():
    """Menu principal"""
    while True:
        print("\n" + "="*60)
        print("🛠️  CONFIGURADOR DE PROVIDERS DE LLM")
        print("="*60)
        print("1. 📦 Instalar providers")
        print("2. 🧪 Testar configuração")
        print("3. 📖 Informações dos providers")
        print("4. 📝 Criar arquivo .env")
        print("5. 🚪 Sair")
        
        try:
            choice = input("\n> Escolha uma opção: ").strip()
            
            if choice == "1":
                setup_provider_installation()
            elif choice == "2":
                test_provider_connection()
            elif choice == "3":
                show_provider_info()
            elif choice == "4":
                create_env_file()
            elif choice == "5":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 