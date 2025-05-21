import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, CreateDateColumn, OneToMany, JoinColumn } from 'typeorm';
import { Usuario } from '../../../src/usuarios/entities/usuario.entity';
import { Grabacion } from '../../../src/grabaciones/entities/grabacion.entity';

@Entity('presentaciones')
export class Presentacion {
  @PrimaryGeneratedColumn()
  id_presentacion: number;

  @ManyToOne(() => Usuario, (usuario) => usuario.id_usuario, { eager: true })
  @JoinColumn({ name: 'id_usuario' })
  usuario: Usuario;

  @Column()
  titulo: string;

  @Column()
  archivo_pdf: string;

  @CreateDateColumn({ type: 'timestamp' })
  fecha_subida: Date;

  @OneToMany(() => Grabacion, (grabacion) => grabacion.presentacion)
  grabaciones: Grabacion[];
}
