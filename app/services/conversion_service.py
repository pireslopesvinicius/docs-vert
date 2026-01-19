import os
import subprocess
import tempfile
from pathlib import Path
from app.core.config import UPLOAD_DIR


class ConversionService:
    """Serviço de conversão de documentos usando LibreOffice"""
    
    def __init__(self):
        self.upload_dir = UPLOAD_DIR
        self.upload_dir.mkdir(exist_ok=True)
        self.libreoffice_path = self._find_libreoffice()
        # Define PATH completo pra systemd
        self.env = os.environ.copy()
        self.env['PATH'] = '/home/docs-vert/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin:/sbin'
    
    def _find_libreoffice(self) -> str:
        """Encontra o caminho do LibreOffice instalado"""
        import platform
        import shutil
        
        # Caminhos padrão por SO
        if platform.system() == "Windows":
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        else:
            # Linux/Mac - tenta AppImage nova primeiro
            if os.path.exists('/usr/local/bin/LibreOffice-fresh.basic-x86_64.AppImage'):
                return '/usr/local/bin/LibreOffice-fresh.basic-x86_64.AppImage'
            
            if shutil.which("soffice"):
                return "soffice"
            if shutil.which("libreoffice"):
                return "libreoffice"
        
        # Tenta usar o comando diretamente
        if shutil.which("soffice"):
            return "soffice"
        
        raise Exception(
            "LibreOffice não encontrado. Por favor, instale LibreOffice: "
            "https://www.libreoffice.org/download/"
        )
    
    async def docx_to_pdf(self, file_contents: bytes, filename: str) -> str:
        """
        Converte arquivo DOCX para PDF usando LibreOffice
        
        Args:
            file_contents: Conteúdo do arquivo DOCX em bytes
            filename: Nome do arquivo original
            
        Returns:
            Caminho do arquivo PDF gerado
        """
        temp_dir = None
        try:
            # Criar diretório temporário
            temp_dir = tempfile.mkdtemp()
            temp_path = Path(temp_dir)
            
            # Salvar arquivo DOCX temporário
            docx_path = temp_path / filename
            docx_path.write_bytes(file_contents)
            
            # Converter para PDF usando LibreOffice
            pdf_filename = filename.replace('.docx', '.pdf')
            
            cmd = [
                self.libreoffice_path,
                "--headless",
                "--convert-to",
                "pdf",
                str(docx_path),
                "--outdir",
                str(temp_path),
            ]
            
            # Executar conversão
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos
                env=self.env
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Erro desconhecido"
                raise Exception(f"Erro na conversão LibreOffice: {error_msg}")
            
            # Encontrar PDF gerado
            pdf_path_temp = temp_path / pdf_filename
            
            if not pdf_path_temp.exists():
                raise Exception(f"PDF não foi gerado em {pdf_path_temp}")
            
            # Mover para diretório final
            final_pdf_path = self.upload_dir / pdf_filename
            
            # Se já existe, deletar antes de mover
            if final_pdf_path.exists():
                final_pdf_path.unlink()
            
            # Usa shutil.move() pq /tmp e /home podem estar em filesystems diferentes
            import shutil
            shutil.move(str(pdf_path_temp), str(final_pdf_path))
            
            return str(final_pdf_path)
        
        except subprocess.TimeoutExpired:
            raise Exception("Conversão excedeu o tempo limite de 5 minutos")
        except Exception as e:
            raise Exception(f"Erro ao converter DOCX para PDF: {str(e)}")
        finally:
            # Limpar arquivos temporários
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"Erro ao limpar diretório temporário: {str(e)}")
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Remove arquivos antigos do diretório de upload"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in self.upload_dir.glob('*.pdf'):
            if current_time - os.path.getmtime(file_path) > max_age_seconds:
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"Erro ao deletar arquivo {file_path}: {str(e)}")

